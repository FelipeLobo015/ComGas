import psycopg2
from db import conectar
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime

# =========================
# Registrar novo botijão
# =========================
def registrar_botijao(usuario_id, litragem, data_inicio, empresa):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Converter data de entrada (dd/mm/yyyy → yyyy-mm-dd)
        data_inicio_fmt = datetime.strptime(data_inicio.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO botijoes (usuario_id, litragem, data_inicio, empresa)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, float(litragem), data_inicio_fmt, empresa))
        conn.commit()

        cursor.close()
        conn.close()
        return f"✅ Botijão de {litragem}kg iniciado em {data_inicio} com sucesso!"

    except Exception as e:
        return f"❌ Erro ao registrar botijão: {e}"

# =========================
# Acompanhar botijões
# =========================
def acompanhar_botijao(usuario_id, somente_ativos=False):
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = """
        SELECT id, litragem, data_inicio, data_fim, empresa
        FROM botijoes
        WHERE usuario_id = %s
        """
        if somente_ativos:
            query += " AND data_fim IS NULL"
        query += " ORDER BY data_inicio DESC"

        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        if not resultados:
            if somente_ativos:
                return "Nenhum botijão ativo encontrado."
            return "Nenhum botijão encontrado."

        texto = "📦 Seus botijões:\n"
        
        # --- INÍCIO DA CORREÇÃO ---
        # Este bloco 'for' foi movido para DENTRO do 'try'
        for linha in resultados:
            id_b, litragem, data_inicio, data_fim, empresa = linha

            # --- Correção data_inicio ---
            # Verifica se data_inicio não é None E se é um objeto date ou datetime
            if data_inicio and isinstance(data_inicio, (date, datetime)):
                data_inicio_str = data_inicio.strftime("%d/%m/%Y")
            else:
                # Se for None ou outro tipo, apenas converte para string
                data_inicio_str = str(data_inicio) if data_inicio else ""

            # --- Correção data_fim (com a regra "em uso") ---
            # Verifica se data_fim não é None E se é um objeto date ou datetime
            if data_fim and isinstance(data_fim, (date, datetime)):
                data_fim_str = data_fim.strftime("%d/%m/%Y")
            else:
                # Se for None ou qualquer valor "falsy", usa "em uso"
                data_fim_str = "em uso"

            # --- Montagem da string ---
            texto += (
                f"ID: {id_b} | Litragem: {litragem}kg | Empresa: {empresa} | "
                f"Início: {data_inicio_str} | Fim: {data_fim_str}\n"
            )

        # Este 'return' também foi movido para DENTRO do 'try'
        return texto
        # --- FIM DA CORREÇÃO ---

    except Exception as e:
        return f"❌ Erro ao acompanhar botijões: {e}"
# =========================
# Gráfico de duração média
# =========================
def gerar_grafico_duracao(usuario_id):
    try:
        conn = conectar()
        query = """
        SELECT litragem, data_inicio, data_fim, empresa
        FROM botijoes
        WHERE usuario_id = %s AND data_fim IS NOT NULL
        """
        df = pd.read_sql_query(query, conn, params=(usuario_id,))
        conn.close()

        if df.empty:
            print("⚠️ Nenhum botijão encerrado para gerar gráfico.")
            return

        df["data_inicio"] = pd.to_datetime(df["data_inicio"], errors="coerce")
        df["data_fim"] = pd.to_datetime(df["data_fim"], errors="coerce")
        df = df.dropna(subset=["data_inicio", "data_fim"])

        if df.empty:
            print("⚠️ Não há registros válidos para gerar gráfico.")
            return

        df["duracao"] = (df["data_fim"] - df["data_inicio"]).dt.days
        
        # Agrupar por 'litragem' E 'empresa'
        df_media = df.groupby(["litragem", "empresa"])["duracao"].mean().reset_index()

        # Criar um rótulo combinado para o eixo X
        df_media["rotulo_eixo_x"] = df_media["litragem"].astype(str) + "kg - " + df_media["empresa"]

        plt.figure(figsize=(6, 4)) # Aumentei o tamanho da figura para melhor visualização
        plt.bar(df_media["rotulo_eixo_x"], df_media["duracao"]) # Usar o novo rótulo combinado
        
        plt.xlabel("Litragem e Empresa") # Mudando o rótulo do eixo X
        plt.ylabel("Duração média (dias)")
        plt.title("Duração média dos botijões por Litragem e Empresa") # Atualizando o título
        
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao gerar gráfico: {e}")

# =========================
# Finalizar botijão
# =========================
def finalizar_botijao(usuario_id, botijao_id, data_fim):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Buscar litragem e data de início
        cursor.execute("""
            SELECT litragem, data_inicio FROM botijoes
            WHERE id = %s AND usuario_id = %s
        """, (botijao_id, usuario_id))
        registro = cursor.fetchone()

        if not registro:
            return "❌ Botijão não encontrado."

        litragem, data_inicio = registro

        # Converter litragem para número
        try:
            litragem = float(litragem)
        except:
            litragem = 0

        # Converter datas
        if isinstance(data_inicio, datetime):
            data_inicio_dt = data_inicio.date()
        else:
            data_inicio_dt = datetime.strptime(str(data_inicio), "%Y-%m-%d").date()

        data_fim_dt = datetime.strptime(data_fim.strip(), "%d/%m/%Y").date()

        # Calcular duração
        duracao = (data_fim_dt - data_inicio_dt).days

        # Atualizar no banco
        cursor.execute("""
            UPDATE botijoes
            SET data_fim = %s
            WHERE id = %s AND usuario_id = %s
        """, (data_fim_dt, botijao_id, usuario_id))
        conn.commit()

        # Definir duração ideal
        if litragem <= 5:
            ideal = 20
        elif litragem <= 13:
            ideal = 60
        else:
            ideal = 90

        # Mensagem de desempenho
        if duracao >= ideal * 0.9:
            msg = f"🟢 Excelente! Seu botijão de {litragem}kg durou {duracao} dias."
        elif duracao >= ideal * 0.6:
            msg = f"🟠 Bom desempenho! Seu botijão durou {duracao} dias."
        else:
            msg = f"🔴 Durou apenas {duracao} dias. Reveja o uso ou verifique vazamentos."

        cursor.close()
        conn.close()
        return msg

    except Exception as e:
        return f"❌ Erro ao finalizar botijão: {e}"
