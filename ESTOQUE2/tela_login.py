import tkinter as tk
from tkinter import messagebox
from banco import conectar
import hashlib
import main

def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha, nivel FROM usuarios WHERE login=?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        senha_hash_armazenada, nivel = resultado
        senha_hash_digitada = hashlib.sha256(senha.encode()).hexdigest()
        if senha_hash_armazenada == senha_hash_digitada:
            return True, nivel
    return False, None

def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    valido, nivel = verificar_login(usuario, senha)
    if valido:
        root.destroy()
        main.abrir_sistema(usuario, nivel)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

root = tk.Tk()
root.title("Login - Sistema de Estoque")
root.geometry("300x180")
root.configure(bg="#1f1f1f")

frame = tk.Frame(root, bg="#1f1f1f")
frame.pack(pady=20)

tk.Label(frame, text="Acesso ao Sistema", font=("Segoe UI", 12, "bold"), bg="#1f1f1f", fg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Usuário:", bg="#1f1f1f", fg="white").grid(row=1, column=0, sticky="w", padx=5)
entry_usuario = tk.Entry(frame)
entry_usuario.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Senha:", bg="#1f1f1f", fg="white").grid(row=2, column=0, sticky="w", padx=5)
entry_senha = tk.Entry(frame, show="*")
entry_senha.grid(row=2, column=1, padx=5, pady=5)

btn_login = tk.Button(frame, text="Entrar", command=fazer_login, bg="#2f62a3", fg="white", width=15)
btn_login.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()