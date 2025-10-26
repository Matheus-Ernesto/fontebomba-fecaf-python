# projeto/bd/create.py
import sqlite3
import os

# Caminho absoluto do banco, independente de onde o script for executado
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "loja.db")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS carrinhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(conta_id) REFERENCES contas(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
)
""")

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
