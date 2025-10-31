from db import conectar

def cadastrar_usuario(nome, senha):
    conn = conectar()
    if not conn:
        print("Não foi possível conectar ao banco.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (nome,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, senha))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False

def login(nome, senha):
    conn = conectar()
    if not conn:
        print("Não foi possível conectar ao banco.")
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        if resultado:
            return resultado[0]  # retorna id do usuário
        else:
            return None
    except Exception as e:
        print(f"Erro no login: {e}")
        return None
