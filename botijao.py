import psycopg2
from db import conectar
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.patches import Patch

# =========================
# Função auxiliar: formata a data automaticamente
# =========================
def parse_data(data_str):
    """
    Converte uma string de data em datetime.
    Aceita formatos comuns: DD/MM/YYYY, D-M-YYYY, DDMMYYYY.
    """
    data_str = str(data_str).strip().replace("-", "/")
    numeros = ''.join(filter(str.isdigit, data_str))
    if len(numeros) == 8:
        dia = numeros[:2]
        mes = numeros[2:4]
        ano = numeros[4:]
        data_formatada = f"{dia}/{mes}/{ano}"
    else:
        data_formatada = data_str

    try:
        return datetime.strptime(data_formatada, "%d/%m/%Y")
    except Exception:
        raise ValueError(f"Data inválida: {data_str}")

# =========================
# Registrar botijão
# =========================
def registrar_botijao(usuario_id, litragem, data_inicial, empresa):
    """
    Registra um novo botijão com eficácia indefinida (NULL).
    """
    try:
        conn = conectar()
        if conn is None:
            print("❌ Falha na conexão com o banco.")
            return

        cursor = conn.cursor()
        query = """
        INSERT INTO botijoes (usuario_id, litragem, data_inicial, eficacia, empresa)
        VALUES (%s, %s, %s, NULL, %s)
        """
        litragem_num = int(litragem)
        data_dt = parse_data(data_inicial)
        empresa_trunc = str(empresa)[:100]

        cursor.execute(query, (usuario_id, litragem_num, data_dt, empresa_trunc))
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
    """
    Mostra todos os botijões registrados por um usuário.
    """
    try:
        conn = conectar()
        if conn is None:
            return "❌ Falha na conexão com o banco."
        cursor = conn.cursor()
        query = """
        SELECT id, litragem, data_inicial, eficacia, empresa
        FROM botijoes
        WHERE usuario_id = %s
        ORDER BY data_inicial DESC
        """
        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        if not resultados:
            return "Nenhum botijão encontrado."

        texto = "📦 Seus botijões:\n"
        for linha in resultados:
            id_b, litragem, data_inicial, eficacia, empresa = linha
            data_str = (
                data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, datetime) else str(data_inicial)
            )
            eficacia_str = f"{eficacia:.2f} kg/dia" if eficacia is not None else "Em uso"
            texto += f"ID: {id_b} | Litragem: {litragem}kg | Empresa: {empresa} | Início: {data_str} | Eficácia: {eficacia_str}\n"

        return texto
    except Exception as e:
        return f"❌ Erro ao acompanhar botijões: {e}"

# =========================
# Gerar gráfico de eficácia
# =========================
def gerar_grafico_duracao(usuario_id):
    """
    Gera um gráfico com o consumo médio (eficácia) de cada botijão finalizado.
    """
    try:
        conn = conectar()
        if conn is None:
            print("❌ Falha na conexão com o banco.")
            return
        query = """
        SELECT id, litragem, eficacia
        FROM botijoes
        WHERE usuario_id = %s AND eficacia IS NOT NULL
        """
        df = pd.read_sql_query(query, conn, params=(usuario_id,))
        conn.close()

        if df.empty:
            print("⚠️ Nenhum botijão finalizado para gerar gráfico.")
            return

        # Definir cores de acordo com eficácia
        cores = []
        for e in df["eficacia"]:
            if e <= 0.43:
                cores.append("green")
            elif e <= 0.70:
                cores.append("gold")
            else:
                cores.append("red")

        # Criar gráfico
        plt.figure(figsize=(7, 5))
        plt.bar(df["id"].astype(str), df["eficacia"], color=cores, edgecolor="black")

        plt.xlabel("ID do Botijão")
        plt.ylabel("Consumo Diário (kg/dia)")
        plt.title("Desempenho dos Botijões de Gás")
        plt.grid(axis="y", linestyle="--", alpha=0.5)

        # Legenda
        legenda = [
            Patch(color="green", label="🟢 Excelente (≤ 0.43 kg/dia)"),
            Patch(color="gold", label="🟡 Médio (0.43–0.70 kg/dia)"),
            Patch(color="red", label="🔴 Excessivo (> 0.70 kg/dia)")
        ]
        plt.legend(handles=legenda, loc="upper left")

        # Mostrar valores
        for i, val in enumerate(df["eficacia"]):
            plt.text(
                i,
                val + 0.01,
                f"{val:.2f} kg/dia",
                ha="center",
                fontsize=9,
                color="black"
            )

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao gerar gráfico: {e}")

# =========================
# Finalizar botijão
# =========================
def finalizar_botijao(usuario_id, botijao_id, data_fim):
    """
    Finaliza um botijão, calcula os dias de uso e a eficácia (kg/dia),
    e salva esse valor no banco.
    """
    try:
        conn = conectar()
        if conn is None:
            return "❌ Falha na conexão com o banco."
        cursor = conn.cursor()

        # Obter litragem e data inicial do botijão
        cursor.execute("""
            SELECT litragem, data_inicial FROM botijoes
            WHERE id = %s AND usuario_id = %s
        """, (botijao_id, usuario_id))
        registro = cursor.fetchone()

        if not registro:
            cursor.close()
            conn.close()
            return "❌ Botijão não encontrado."

        litragem, data_inicial = registro
        data_fim_dt = parse_data(data_fim)
        data_inicio_dt = (
            data_inicial if isinstance(data_inicial, datetime)
            else datetime.strptime(str(data_inicial), "%Y-%m-%d")
        )

        # Calcular dias de uso
        dias_uso = (data_fim_dt - data_inicio_dt).days
        if dias_uso <= 0:
            cursor.close()
            conn.close()
            return "❌ Data final inválida (anterior ou igual à inicial)."

        # Calcular eficácia = peso (kg) / dias de uso
        eficacia = round(float(litragem) / dias_uso, 2)

        # Atualizar eficácia no banco
        cursor.execute("""
            UPDATE botijoes
            SET eficacia = %s
            WHERE id = %s AND usuario_id = %s
        """, (eficacia, botijao_id, usuario_id))
        conn.commit()

        # Avaliação de desempenho
        if eficacia <= 0.43:
            msg = f"🟢 Excelente! Consumo médio de {eficacia:.2f} kg/dia."
        elif eficacia <= 0.70:
            msg = f"🟡 Bom desempenho. Consumo médio de {eficacia:.2f} kg/dia."
        else:
            msg = f"🔴 Gasto elevado ({eficacia:.2f} kg/dia). Verifique possíveis desperdícios."

        cursor.close()
        conn.close()
        return msg

    except Exception as e:
        return f"❌ Erro ao finalizar botijão: {e}"
