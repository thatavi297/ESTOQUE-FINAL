# 🔒 Proteção: impede execução direta
if __name__ == "__main__":
    print("⚠️ Este módulo não deve ser executado diretamente.")
    exit()

import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar
import hashlib

def carregar_tela_usuarios(frame_pai, nivel_usuario_logado):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    frame_pai.columnconfigure((0,1,2,3), weight=1)
    frame_pai.rowconfigure(2, weight=1)

    ttk.Label(frame_pai, text="Gerenciar Usuários", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    entry_nome = ttk.Entry(frame_pai)
    entry_nome.insert(0, "Nome")
    entry_nome.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    entry_login = ttk.Entry(frame_pai)
    entry_login.insert(0, "Login")
    entry_login.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    entry_senha = ttk.Entry(frame_pai, show="*")
    entry_senha.insert(0, "Senha")
    entry_senha.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

    combo_nivel = ttk.Combobox(frame_pai, values=["Administrador", "Comum"], state="readonly")
    combo_nivel.set("Comum")
    combo_nivel.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    tree = ttk.Treeview(frame_pai, columns=("ID", "Nome", "Login", "Nível"), show="headings")
    for col in ("ID", "Nome", "Login", "Nível"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, login, nivel FROM usuarios")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def limpar():
        entry_nome.delete(0, tk.END)
        entry_login.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        combo_nivel.set("Comum")

    def adicionar():
        if nivel_usuario_logado != "Administrador":
            messagebox.showwarning("Permissão negada", "Apenas administradores podem adicionar usuários.")
            return
        nome = entry_nome.get()
        login = entry_login.get()
        senha = entry_senha.get()
        nivel = combo_nivel.get()
        if not nome or not login or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, login, senha, nivel) VALUES (?, ?, ?, ?)", (nome, login, senha_hash, nivel))
            conn.commit()
            conn.close()
            atualizar_tabela()
            limpar()
        except:
            messagebox.showerror("Erro", "Login já existente.")

    def excluir():
        if nivel_usuario_logado != "Administrador":
            messagebox.showwarning("Permissão negada", "Apenas administradores podem excluir usuários.")
            return
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
            return
        usuario_id = tree.item(item)["values"][0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        atualizar_tabela()

    ttk.Button(frame_pai, text="➕ Adicionar", command=adicionar).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    if nivel_usuario_logado == "Administrador":
        ttk.Button(frame_pai, text="🗑️ Excluir", command=excluir).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    atualizar_tabela()