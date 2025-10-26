# projeto/bd/insert.py
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "loja.db")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.executemany("""
INSERT INTO contas (nome, email, senha)
VALUES (?, ?, ?)
""", [
    ("Matheus", "matheus@email.com", "1234"),
    ("Ana", "ana@email.com", "4321")
])

cur.executemany("""
INSERT INTO produtos (nome, preco, estoque)
VALUES (?, ?, ?)
""", [
    ("Mouse Gamer", 99.90, 10),
    ("Teclado Mecânico", 199.90, 5),
    ("Headset RGB", 149.90, 7)
])

con.commit()
con.close()
print("✅ Dados inseridos no banco:", DB_PATH)
