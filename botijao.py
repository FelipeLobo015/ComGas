import psycopg2
from db import conectar
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# =========================
# Registrar botijão
# =========================
def registrar_botijao(usuario_id, litragem, data_inicio, empresa):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO botijoes (usuario_id, litragem, data_inicio, empresa)
        VALUES (%s, %s, %s, %s)
        """
        # Converte litragem para float e string curta
        litragem_num = str(float(litragem))[:10]
        data_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
        cursor.execute(query, (usuario_id, str(litragem), data_dt, empresa))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Botijão registrado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao registrar botijão: {e}")

# =========================
# Acompanhar botijões
# =========================
def acompanhar_botijao(usuario_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT id, litragem, data_inicio, data_fim, empresa
        FROM botijoes
        WHERE usuario_id = %s
        ORDER BY data_inicio DESC
        """
        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        if not resultados:
            return "Nenhum botijão encontrado."

        texto = "📦 Seus botijões:\n"
        for linha in resultados:
            id_b, litragem, data_inicio, data_fim, empresa = linha
            data_inicio_str = (
                data_inicio.strftime("%d/%m/%Y") if isinstance(data_inicio, datetime) else str(data_inicio)
            )
            data_fim_str = (
                data_fim.strftime("%d/%m/%Y") if isinstance(data_fim, datetime) else "Em uso"
            )
            texto += f"ID: {id_b} | Litragem: {litragem}kg | Empresa: {empresa} | Início: {data_inicio_str} | Fim: {data_fim_str}\n"

        return texto

    except Exception as e:
        return f"❌ Erro ao acompanhar botijões: {e}"

# =========================
# Gráfico de duração média
# =========================
def gerar_grafico_duracao(usuario_id):
    try:
        conn = conectar()
        query = """
        SELECT litragem, data_inicio, data_fim
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
        df_media = df.groupby("litragem")["duracao"].mean().reset_index()

        plt.figure(figsize=(6, 4))
        plt.bar(df_media["litragem"].astype(str), df_media["duracao"])
        plt.xlabel("Litragem (kg)")
        plt.ylabel("Duração média (dias)")
        plt.title("Duração média dos botijões por litragem")
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

        # Pega a data de início
        cursor.execute("""
            SELECT litragem, data_inicio FROM botijoes
            WHERE id = %s AND usuario_id = %s
        """, (botijao_id, usuario_id))
        registro = cursor.fetchone()

        if not registro:
            return "❌ Botijão não encontrado."

        litragem, data_inicio = registro
        data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
        data_inicio_dt = (
            data_inicio if isinstance(data_inicio, datetime)
            else datetime.strptime(str(data_inicio), "%Y-%m-%d")
        )

        duracao = (data_fim_dt - data_inicio_dt).days

        # Atualizar no banco
        cursor.execute("""
            UPDATE botijoes
            SET data_fim = %s
            WHERE id = %s AND usuario_id = %s
        """, (data_fim_dt, botijao_id, usuario_id))
        conn.commit()

        # Avaliação
        if litragem <= 5:
            ideal = 20
        elif litragem <= 13:
            ideal = 60
        else:
            ideal = 90

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
