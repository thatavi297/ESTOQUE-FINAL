# banco.py
import sqlite3
import hashlib

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        login TEXT UNIQUE,
        senha TEXT,
        nivel TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        estoque INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        data TEXT,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    # Verifica se o admin já existe
    cursor.execute("SELECT * FROM usuarios WHERE login = 'admin'")
    if not cursor.fetchone():
        senha_hash = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (nome, login, senha, nivel) VALUES (?, ?, ?, ?)",
                       ("Administrador", "admin", senha_hash, "Administrador"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("✅ Banco de dados e tabelas criados com sucesso.")
