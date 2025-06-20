# 🔒 Proteção: impede execução direta
if __name__ == "__main__":
    print("⚠️ Este módulo não deve ser executado diretamente.")
    exit()

import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def carregar_tela_produtos(frame_pai, nivel_usuario_logado):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    frame_pai.columnconfigure((0,1,2,3), weight=1)
    frame_pai.rowconfigure(2, weight=1)

    ttk.Label(frame_pai, text="Gerenciar Produtos", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10))

    entry_nome = ttk.Entry(frame_pai)
    entry_nome.insert(0, "Nome")
    entry_nome.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    entry_preco = ttk.Entry(frame_pai)
    entry_preco.insert(0, "Preço")
    entry_preco.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    entry_estoque = ttk.Entry(frame_pai)
    entry_estoque.insert(0, "Estoque")
    entry_estoque.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def limpar():
        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_estoque.delete(0, tk.END)

    def adicionar():
        if nivel_usuario_logado != "Administrador":
            messagebox.showwarning("Permissão negada", "Apenas administradores podem adicionar produtos.")
            return
        nome = entry_nome.get()
        try:
            preco = float(entry_preco.get())
            estoque = int(entry_estoque.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Preço ou estoque inválido.")
            return
        if not nome:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    def remover():
        if nivel_usuario_logado != "Administrador":
            messagebox.showwarning("Permissão negada", "Apenas administradores podem remover produtos.")
            return
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return
        produto_id = tree.item(item)["values"][0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        conn.close()
        atualizar_tabela()

    def editar():
        if nivel_usuario_logado != "Administrador":
            messagebox.showwarning("Permissão negada", "Apenas administradores podem editar produtos.")
            return
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return
        produto_id = tree.item(item)["values"][0]
        nome = entry_nome.get()
        try:
            preco = float(entry_preco.get())
            estoque = int(entry_estoque.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Preço ou estoque inválido.")
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET nome = ?, preco = ?, estoque = ? WHERE id = ?", (nome, preco, estoque, produto_id))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    ttk.Button(frame_pai, text="➕ Adicionar", command=adicionar).grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    ttk.Button(frame_pai, text="✏️ Editar", command=editar).grid(row=2, column=3, padx=5, pady=5, sticky="ew")
    ttk.Button(frame_pai, text="🗑️ Remover", command=remover).grid(row=3, column=3, padx=5, pady=5, sticky="ew")

    tree = ttk.Treeview(frame_pai, columns=("ID", "Nome", "Preço", "Estoque"), show="headings")
    for col in ("ID", "Nome", "Preço", "Estoque"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10)

    atualizar_tabela()