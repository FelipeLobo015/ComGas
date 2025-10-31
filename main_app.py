import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from user import cadastrar_usuario, login
from botijao import registrar_botijao, acompanhar_botijao, gerar_grafico_duracao, finalizar_botijao

# ===== CONFIGURAÇÃO =====
usuario_id = None

# ===== JANELA PRINCIPAL =====
root = tk.Tk()
root.title("Monitor de Botijões - UPX 3")
root.geometry("900x700")

# ===== FRAMES =====
frame_login = tk.Frame(root)
frame_menu = tk.Frame(root)
frame_registro = tk.Frame(root)
frame_acompanhamento = tk.Frame(root)

# ===== FUNÇÕES =====
def mostrar_frame(frame):
    for f in [frame_login, frame_menu, frame_registro, frame_acompanhamento]:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ===== LOGIN E CADASTRO =====
def fazer_login():
    global usuario_id
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    usuario_id = login(usuario, senha)
    if usuario_id:
        messagebox.showinfo("Login", f"Bem-vindo, {usuario}!")
        mostrar_frame(frame_menu)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def registrar():
    nome = entry_novo_usuario.get().strip()
    senha = entry_nova_senha.get().strip()
    if not nome or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return
    cadastrar_usuario(nome, senha)
    messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
    mostrar_frame(frame_login)

# ===== REGISTRAR BOTIJÃO =====
def abrir_registro_botijao():
    mostrar_frame(frame_registro)

def registrar_botijao_gui():
    global usuario_id
    if not usuario_id:
        messagebox.showerror("Erro", "Faça login primeiro!")
        return
    capacidade = entry_capacidade.get().strip()
    empresa = entry_empresa.get().strip()
    data_inicio = entry_inicio.get().strip()
    if not (capacidade and empresa and data_inicio):
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return
    try:
        float(capacidade)  # garante número
    except:
        messagebox.showerror("Erro", "Litragem deve ser um número.")
        return
    registrar_botijao(usuario_id, capacidade, data_inicio, empresa)
    messagebox.showinfo("Registro", "Botijão registrado com sucesso!")
    entry_capacidade.delete(0, tk.END)
    entry_empresa.delete(0, tk.END)
    entry_inicio.delete(0, tk.END)
    mostrar_frame(frame_menu)

# ===== ACOMPANHAMENTO =====
def abrir_acompanhamento():
    global usuario_id
    if not usuario_id:
        messagebox.showerror("Erro", "Faça login primeiro!")
        return
    texto = acompanhar_botijao(usuario_id)
    text_acompanhamento.delete("1.0", tk.END)
    text_acompanhamento.insert(tk.END, texto)
    mostrar_frame(frame_acompanhamento)

# ===== FINALIZAR BOTIJÃO =====
def finalizar_botijao_app():
    global usuario_id
    if not usuario_id:
        messagebox.showerror("Erro", "Faça login primeiro!")
        return

    # Pega botijões disponíveis
    conn_text = acompanhar_botijao(usuario_id)
    linhas = [l for l in conn_text.split("\n") if l.startswith("ID:")]
    if not linhas:
        messagebox.showinfo("Info", "Nenhum botijão disponível para finalizar.")
        return

    def confirmar_finalizacao():
        selecao = combo_botijao.get()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um botijão.")
            return
        botijao_id = selecao.split("|")[0].replace("ID:","").strip()
        data_fim = entry_data.get().strip()
        if not data_fim:
            messagebox.showerror("Erro", "Informe a data de término.")
            return
        msg = finalizar_botijao(usuario_id, botijao_id, data_fim)
        messagebox.showinfo("Resultado", msg)
        janela_finalizar.destroy()

    janela_finalizar = Toplevel(root)
    janela_finalizar.title("Finalizar Botijão")
    janela_finalizar.geometry("400x250")

    tk.Label(janela_finalizar, text="Selecione o Botijão:").pack(pady=5)
    combo_botijao = ttk.Combobox(janela_finalizar, width=50, values=linhas)
    combo_botijao.pack(pady=5)

    tk.Label(janela_finalizar, text="Data de Término (DD/MM/AAAA):").pack(pady=5)
    entry_data = tk.Entry(janela_finalizar, width=20)
    entry_data.pack(pady=5)

    tk.Button(janela_finalizar, text="Finalizar", command=confirmar_finalizacao, width=25).pack(pady=20)

# ===== GERAR GRÁFICO =====
def abrir_graficos():
    global usuario_id
    if not usuario_id:
        messagebox.showerror("Erro", "Faça login primeiro!")
        return
    gerar_grafico_duracao(usuario_id)
    messagebox.showinfo("Gráfico", "Gráfico gerado com sucesso (veja a janela matplotlib).")

# =========================
# ===== TELA LOGIN =======
# =========================
tk.Label(frame_login, text="Login", font=("Arial", 22, "bold")).pack(pady=30)
tk.Label(frame_login, text="Usuário").pack()
entry_usuario = tk.Entry(frame_login, width=30)
entry_usuario.pack(pady=5)
tk.Label(frame_login, text="Senha").pack()
entry_senha = tk.Entry(frame_login, show="*", width=30)
entry_senha.pack(pady=5)
tk.Button(frame_login, text="Entrar", width=25, command=fazer_login).pack(pady=15)
tk.Label(frame_login, text="Novo por aqui? Cadastre-se abaixo:").pack(pady=10)
tk.Label(frame_login, text="Novo usuário").pack()
entry_novo_usuario = tk.Entry(frame_login, width=30)
entry_novo_usuario.pack(pady=5)
tk.Label(frame_login, text="Nova senha").pack()
entry_nova_senha = tk.Entry(frame_login, show="*", width=30)
entry_nova_senha.pack(pady=5)
tk.Button(frame_login, text="Cadastrar", width=25, command=registrar).pack(pady=15)

# =========================
# ===== MENU PRINCIPAL ====
# =========================
tk.Label(frame_menu, text="Menu Principal", font=("Arial", 20, "bold")).pack(pady=30)
tk.Button(frame_menu, text="Registrar Botijão", command=abrir_registro_botijao, width=30).pack(pady=10)
tk.Button(frame_menu, text="Finalizar Botijão", command=finalizar_botijao_app, width=30).pack(pady=10)
tk.Button(frame_menu, text="Acompanhar Botijão", command=abrir_acompanhamento, width=30).pack(pady=10)
tk.Button(frame_menu, text="Gerar Gráfico de Duração", command=abrir_graficos, width=30).pack(pady=10)
tk.Button(frame_menu, text="Sair", command=lambda: mostrar_frame(frame_login), width=30).pack(pady=10)

# =========================
# ===== REGISTRO BOTIJÃO ===
# =========================
tk.Label(frame_registro, text="Registrar Novo Botijão", font=("Arial", 18, "bold")).pack(pady=25)
tk.Label(frame_registro, text="Capacidade (kg)").pack()
entry_capacidade = tk.Entry(frame_registro, width=30)
entry_capacidade.pack(pady=5)
tk.Label(frame_registro, text="Empresa").pack()
entry_empresa = tk.Entry(frame_registro, width=30)
entry_empresa.pack(pady=5)
tk.Label(frame_registro, text="Data Início (DD/MM/AAAA)").pack()
entry_inicio = tk.Entry(frame_registro, width=30)
entry_inicio.pack(pady=5)
tk.Button(frame_registro, text="Registrar", command=registrar_botijao_gui, width=25).pack(pady=15)
tk.Button(frame_registro, text="Voltar", command=lambda: mostrar_frame(frame_menu), width=25).pack(pady=5)

# =========================
# ===== ACOMPANHAMENTO ====
# =========================
tk.Label(frame_acompanhamento, text="Acompanhar Botijões", font=("Arial", 18, "bold")).pack(pady=20)
text_acompanhamento = tk.Text(frame_acompanhamento, width=100, height=25, wrap="word", font=("Consolas", 10))
text_acompanhamento.pack(pady=10)
tk.Button(frame_acompanhamento, text="Voltar", command=lambda: mostrar_frame(frame_menu), width=25).pack(pady=10)

# =========================
# ===== INICIAL ===========
# =========================
mostrar_frame(frame_login)

# ===== LOOP PRINCIPAL =====
root.mainloop()
