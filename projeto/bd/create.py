import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "loja.db")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Contas (usuários)
cur.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

# Produtos
cur.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL,
    estoque INTEGER NOT NULL
)
""")

# Carrinhos
cur.execute("""
CREATE TABLE IF NOT EXISTS carrinhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    FOREIGN KEY(conta_id) REFERENCES contas(id)
)
""")

# Relação carrinho-produto (N:N)
cur.execute("""
CREATE TABLE IF NOT EXISTS carrinhos_produtos (
    carrinho_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY(carrinho_id) REFERENCES carrinhos(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id),
    PRIMARY KEY(carrinho_id, produto_id)
)
""")

# Compras (histórico de pedidos)
cur.execute("""
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY(conta_id) REFERENCES contas(id)
)
""")

con.commit()
con.close()
print("✅ Banco criado em:", DB_PATH)