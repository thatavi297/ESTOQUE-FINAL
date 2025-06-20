import tkinter as tk
from tkinter import ttk
import produtos
import movimentacoes
import usuarios
import relatorio

def abrir_sistema(usuario, nivel_usuario):
    app = tk.Tk()
    app.title("Sistema de Controle de Estoque")
    app.geometry("900x500")
    app.configure(bg="#1f1f1f")

    frame_menu = tk.Frame(app, bg="#1f1f1f")
    frame_menu.pack(side="left", fill="y", padx=10, pady=10)

    frame_conteudo = tk.Frame(app, bg="#2f2f2f")
    frame_conteudo.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame_menu, text="Menu", font=("Segoe UI", 12, "bold"), background="#1f1f1f", foreground="white").pack(pady=10)

    def mostrar_produtos():
        produtos.carregar_tela_produtos(frame_conteudo, nivel_usuario)

    def mostrar_movimentacoes():
        movimentacoes.carregar_tela_movimentacoes(frame_conteudo, usuario)

    def mostrar_usuarios():
        usuarios.carregar_tela_usuarios(frame_conteudo, nivel_usuario)

    def mostrar_relatorio():
        relatorio.carregar_tela_relatorio(frame_conteudo)

    def sair():
        app.destroy()

    ttk.Button(frame_menu, text="🛒 Produtos", width=18, command=mostrar_produtos).pack(pady=5)
    ttk.Button(frame_menu, text="📄 Movimentações", width=18, command=mostrar_movimentacoes).pack(pady=5)
    if nivel_usuario == "Administrador":
        ttk.Button(frame_menu, text="👤 Usuários", width=18, command=mostrar_usuarios).pack(pady=5)
    ttk.Button(frame_menu, text="📊 Relatório", width=18, command=mostrar_relatorio).pack(pady=5)
    ttk.Button(frame_menu, text="⏻ Sair", width=18, command=sair).pack(pady=20)

    app.mainloop()