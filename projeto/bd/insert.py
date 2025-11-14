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
    ("Matheus", "matheus@email.com", "1234"),
    ("Ana", "ana@email.com", "4321"),
    ("Pedro", "pedro@email.com", "sorvete")
])

# Inserir produtos (ordem correta: nome, preco, descricao, estoque)
cur.executemany("""
INSERT INTO produtos (nome, preco, descricao, estoque)
VALUES (?, ?, ?, ?)
""", [
    ("Mouse Gamer", 99.90, "Mouse gamer RGB com 6 botões", 10),
    ("Teclado Mecânico", 199.90, "Teclado mecânico com switches blue", 5),
    ("Headset RGB", 149.90, "Headset com som 7.1 e microfone retrátil", 7)
])

# Buscar ID do usuário "Matheus"
cur.execute("SELECT id FROM contas WHERE nome = ?", ("Matheus",))
matheus_id = cur.fetchone()[0]

# Criar um carrinho para o Matheus
cur.execute("""
INSERT INTO carrinhos (conta_id)
VALUES (?)
""", (matheus_id,))
carrinho_id = cur.lastrowid  # pega o ID do carrinho recém-criado

# Buscar IDs dos produtos
cur.execute("SELECT id FROM produtos WHERE nome = 'Mouse Gamer'")
mouse_id = cur.fetchone()[0]

cur.execute("SELECT id FROM produtos WHERE nome = 'Headset RGB'")
headset_id = cur.fetchone()[0]

# Inserir produtos no carrinho do Matheus
cur.executemany("""
INSERT INTO carrinhos_produtos (carrinho_id, produto_id, quantidade, preco)
VALUES (?, ?, ?, ?)
""", [
    (carrinho_id, mouse_id, 1, 99.90),
    (carrinho_id, headset_id, 2, 149.90)
])

con.commit()
con.close()
print("✅ Dados inseridos no banco:", DB_PATH)
print(f"🛒 Carrinho de Matheus criado (id: {carrinho_id}) com 2 produtos.")
