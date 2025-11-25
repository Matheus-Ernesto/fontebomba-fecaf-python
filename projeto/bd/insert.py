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
INSERT INTO produtos (nome, preco, descricao, estoque, imagem)
VALUES (?, ?, ?, ?, ?)
""", [
    ("Smartphone Samsung Galaxy A54", 1899.99, "Um smartphone moderno com ótimo desempenho e câmera de alta qualidade.", 15, "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop"),
    ("Notebook Lenovo IdeaPad", 2999.90, "Notebook ideal para estudos, trabalho e tarefas do dia a dia.", 20, "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&h=400&fit=crop"),
    ("Smart TV LG 50 4K", 2299.00, "TV 4K com excelente qualidade de imagem e recursos inteligentes.", 10, "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=400&fit=crop"),
    ("Tênis Nike Air Max", 399.99, "Tênis confortável e estiloso, ideal para o dia a dia.", 25, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"),
    ("Fone JBL Bluetooth", 199.90, "Fone Bluetooth com excelente qualidade sonora e bateria duradoura.", 30, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"),
    ("Setup de Computador Gamer", 899.00, "Setup de computador Gamer.", 18, "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=400&h=400&fit=crop"),
    ("Console PlayStation 5", 3999.99, "Console de última geração com desempenho impressionante.", 5, "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop"),
    ("Apple Watch Series 8", 2899.00, "Relógio inteligente com monitoramento avançado de saúde.", 12, "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop"),
    ("Tablet Samsung Galaxy Tab", 2199.90, "Tablet versátil ideal para estudo, trabalho e entretenimento.", 15, "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400&h=400&fit=crop"),
    ("Câmera Canon EOS Rebel", 2699.00, "Câmera DSLR perfeita para iniciantes e entusiastas da fotografia.", 8, "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop"),
    ("Mouse Gamer Logitech", 249.90, "Mouse gamer preciso com iluminação e alta durabilidade.", 20, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"),
    ("Teclado Mecânico RGB", 449.90, "Teclado mecânico com iluminação RGB e switches de alta performance.", 22, "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop")
])


# Buscar ID do usuário "Matheus"
cur.execute("SELECT id FROM contas WHERE nome = ?", ("Matheus",))
matheus_id = cur.fetchone()[0]

# Buscar IDs dos produtos
cur.execute("SELECT id FROM produtos WHERE nome = 'Smartphone Samsung Galaxy A54'")
mouse_id = cur.fetchone()[0]

cur.execute("SELECT id FROM produtos WHERE nome = 'Teclado Mecânico RGB'")
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
