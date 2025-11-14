# projeto/bd/insert.py
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "loja.db")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Inserir contas
cur.executemany("""
INSERT INTO contas (nome, email, senha)
VALUES (?, ?, ?)
""", [
    ("Matheus", "matheus@email.com", "123"),
    ("Pedro", "pedro@email.com", "456")
])

# Inserir produtos
cur.executemany("""
INSERT INTO produtos (nome, preco, descricao, estoque)
VALUES (?, ?, ?, ?)
""", [
    ("Mouse Gamer", 99.90, "Mouse gamer", 10),
    ("Teclado Mecânico", 199.90, "Teclado mecânico com switches blue", 5),
    ("Headset", 149.90, "Headset com som 7.1 e microfone retrátil", 7)
])

# Buscar ID do usuário "Matheus"
cur.execute("SELECT id FROM contas WHERE nome = ?", ("Matheus",))
matheus_id = cur.fetchone()[0]

# Buscar IDs dos produtos
cur.execute("SELECT id FROM produtos WHERE nome = 'Mouse Gamer'")
mouse_id = cur.fetchone()[0]

cur.execute("SELECT id FROM produtos WHERE nome = 'Headset'")
headset_id = cur.fetchone()[0]

# Inserir itens no carrinho do Matheus
cur.executemany("""
INSERT INTO carrinho_itens (conta_id, produto_id, quantidade, preco)
VALUES (?, ?, ?, ?)
""", [
    (matheus_id, mouse_id, 1, 99.90),
    (matheus_id, headset_id, 2, 149.90)
])

con.commit()
con.close()

print("✅ Dados inseridos no banco:", DB_PATH)
print("🛒 Carrinho de Matheus criado com 2 produtos.")
