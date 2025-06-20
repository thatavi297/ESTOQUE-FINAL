# 🔒 Proteção: impede execução direta
if __name__ == "__main__":
    print("⚠️ Este módulo não deve ser executado diretamente.")
    exit()

import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar
from datetime import datetime

def carregar_tela_movimentacoes(frame_pai, usuario_logado):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    frame_pai.columnconfigure((0,1,2,3), weight=1)
    frame_pai.rowconfigure(3, weight=1)

    ttk.Label(frame_pai, text="Registrar Movimentação", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

    ttk.Label(frame_pai, text="Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_produto = ttk.Combobox(frame_pai, state="readonly")
    combo_produto.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_pai, text="Tipo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    combo_tipo = ttk.Combobox(frame_pai, values=["Entrada", "Saída"], state="readonly")
    combo_tipo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_pai, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_qtd = ttk.Entry(frame_pai)
    entry_qtd.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def carregar_produtos():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM produtos")
        produtos = cursor.fetchall()
        combo_produto['values'] = [f"{id} - {nome}" for id, nome in produtos]
        conn.close()

    def registrar():
        if not combo_produto.get() or not combo_tipo.get() or not entry_qtd.get():
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        try:
            quantidade = int(entry_qtd.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade inválida.")
            return

        produto_id = int(combo_produto.get().split(" - ")[0])
        tipo = combo_tipo.get()
        data = datetime.now().strftime("%Y-%m-%d")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?, ?, ?, ?)", (produto_id, tipo, quantidade, data))
        if tipo == "Entrada":
            cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (quantidade, produto_id))
        else:
            cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (quantidade, produto_id))
        conn.commit()
        conn.close()
        atualizar_tabela()
        entry_qtd.delete(0, tk.END)

    ttk.Button(frame_pai, text="➕ Registrar", command=registrar).grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    tree = ttk.Treeview(frame_pai, columns=("ID", "Produto", "Tipo", "Quantidade", "Data"), show="headings")
    for col in ("ID", "Produto", "Tipo", "Quantidade", "Data"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, p.nome, m.tipo, m.quantidade, m.data
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            ORDER BY m.data DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    carregar_produtos()
    atualizar_tabela()