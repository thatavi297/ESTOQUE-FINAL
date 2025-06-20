# 🔒 Proteção: impede execução direta
if __name__ == "__main__":
    print("⚠️ Este módulo não deve ser executado diretamente.")
    exit()

import tkinter as tk
from tkinter import ttk
from banco import conectar

def carregar_tela_relatorio(frame_pai):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    ttk.Label(frame_pai, text="Relatório de Movimentações", font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame_filtros = ttk.Frame(frame_pai)
    frame_filtros.pack(pady=10)

    ttk.Label(frame_filtros, text="Filtrar por mês:").grid(row=0, column=0, padx=5)
    combo_mes = ttk.Combobox(frame_filtros, state="readonly", width=20)
    combo_mes.grid(row=0, column=1, padx=5)

    def carregar_meses():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%m/%Y', data) FROM movimentacoes ORDER BY data DESC")
        meses = [linha[0] for linha in cursor.fetchall()]
        conn.close()
        combo_mes["values"] = meses

    frame_resultado = ttk.Frame(frame_pai)
    frame_resultado.pack(pady=10)

    lbl_entradas = ttk.Label(frame_resultado, text="Total de Entradas: R$ 0,00", font=("Segoe UI", 10, "bold"))
    lbl_entradas.pack(anchor="w", padx=10)

    lbl_saidas = ttk.Label(frame_resultado, text="Total de Saídas: R$ 0,00", font=("Segoe UI", 10, "bold"))
    lbl_saidas.pack(anchor="w", padx=10)

    lbl_saldo = ttk.Label(frame_resultado, text="Saldo Final: R$ 0,00", font=("Segoe UI", 10, "bold"))
    lbl_saldo.pack(anchor="w", padx=10)

    def gerar_relatorio():
        mes = combo_mes.get()
        if not mes:
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.tipo, m.quantidade, p.preco
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE strftime('%m/%Y', m.data) = ?
        """, (mes,))
        entradas = 0
        saidas = 0
        for tipo, qtd, preco in cursor.fetchall():
            total = qtd * preco
            if tipo == "Entrada":
                entradas += total
            else:
                saidas += total
        saldo = entradas - saidas
        lbl_entradas.config(text=f"Total de Entradas: R$ {entradas:,.2f}".replace(".", ","))
        lbl_saidas.config(text=f"Total de Saídas: R$ {saidas:,.2f}".replace(".", ","))
        lbl_saldo.config(text=f"Saldo Final: R$ {saldo:,.2f}".replace(".", ","))
        conn.close()

    ttk.Button(frame_filtros, text="Gerar Relatório", command=gerar_relatorio).grid(row=0, column=2, padx=5)
    carregar_meses()