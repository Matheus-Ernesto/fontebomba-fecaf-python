# Comando para rodar a API
# uvicorn api:app --reload

# projeto/api/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# -----------------------------
# CONFIGURAÇÃO BÁSICA
# -----------------------------
app = FastAPI(title="API Loja", version="1.0")

# CORS (libera acesso do front-end)
origins = ["*"]  # pode restringir depois
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho absoluto para o banco
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sobe de /api para /projeto
DB_PATH = os.path.join(BASE_DIR, "bd", "loja.db")

def conectar():
    return sqlite3.connect(DB_PATH)

# -----------------------------
# MODELOS Pydantic
# -----------------------------
class Login(BaseModel):
    email: str
    senha: str

class AtualizarEmail(BaseModel):
    id: int
    novo_email: str

class AtualizarSenha(BaseModel):
    id: int
    nova_senha: str

class CarrinhoItem(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int = 1

# -----------------------------
# ROTAS BÁSICAS
# -----------------------------
@app.get("/")
def home():
    return {"mensagem": "🛍️ API da Loja funcionando!"}

@app.get("/produtos")
def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, preco, descricao, estoque FROM produtos")
    dados = cur.fetchall()
    con.close()
    return [
        {"id": d[0], "nome": d[1], "preco": d[2], "descricao": d[3], "estoque": d[4]}
        for d in dados
    ]

@app.get("/contas")
def listar_contas():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, email FROM contas")
    dados = cur.fetchall()
    con.close()
    return [{"id": d[0], "nome": d[1], "email": d[2]} for d in dados]

# -----------------------------
# LOGIN E CONTA
# -----------------------------
@app.post("/login")
def login(dados: Login):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT id, nome FROM contas WHERE email = ? AND senha = ?",
        (dados.email, dados.senha)
    )
    usuario = cur.fetchone()
    con.close()
    
    if usuario:
        return {"id": usuario[0], "nome": usuario[1]}
    else:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

@app.put("/conta/email")
def atualizar_email(dados: AtualizarEmail):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("UPDATE contas SET email = ? WHERE id = ?", (dados.novo_email, dados.id))
        con.commit()
        return {"mensagem": "Email atualizado com sucesso!"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.put("/conta/senha")
def atualizar_senha(dados: AtualizarSenha):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("UPDATE contas SET senha = ? WHERE id = ?", (dados.nova_senha, dados.id))
        con.commit()
        return {"mensagem": "Senha atualizada com sucesso!"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

# -----------------------------
# CARRINHO
# -----------------------------
@app.get("/carrinho/{usuario_id}")
def listar_carrinho(usuario_id: int):
    con = conectar()
    cur = con.cursor()

    # Busca o carrinho do usuário
    cur.execute("SELECT id FROM carrinhos WHERE conta_id = ?", (usuario_id,))
    carrinho = cur.fetchone()
    if not carrinho:
        con.close()
        return {"mensagem": "Carrinho vazio", "itens": []}

    carrinho_id = carrinho[0]

    # Busca produtos vinculados ao carrinho
    cur.execute("""
        SELECT p.id, p.nome, cp.preco, cp.quantidade
        FROM carrinhos_produtos cp
        JOIN produtos p ON cp.produto_id = p.id
        WHERE cp.carrinho_id = ?
    """, (carrinho_id,))

    itens = cur.fetchall()
    con.close()

    total = sum(i[2] * i[3] for i in itens)

    return {
        "carrinho_id": carrinho_id,
        "total": total,
        "itens": [
            {"produto_id": i[0], "nome": i[1], "preco": i[2], "quantidade": i[3]}
            for i in itens
        ]
    }

@app.post("/carrinho")
def adicionar_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()
    try:
        # Verifica se o usuário já tem carrinho
        cur.execute("SELECT id FROM carrinhos WHERE conta_id = ?", (item.usuario_id,))
        carrinho = cur.fetchone()

        # Se não existir, cria um novo carrinho
        if not carrinho:
            cur.execute("INSERT INTO carrinhos (conta_id) VALUES (?)", (item.usuario_id,))
            carrinho_id = cur.lastrowid
        else:
            carrinho_id = carrinho[0]

        # Verifica se o produto já está no carrinho
        cur.execute("""
            SELECT quantidade FROM carrinhos_produtos
            WHERE carrinho_id = ? AND produto_id = ?
        """, (carrinho_id, item.produto_id))
        existente = cur.fetchone()

        if existente:
            nova_qtde = existente[0] + item.quantidade
            cur.execute("""
                UPDATE carrinhos_produtos
                SET quantidade = ?
                WHERE carrinho_id = ? AND produto_id = ?
            """, (nova_qtde, carrinho_id, item.produto_id))
        else:
            # Pega o preço atual do produto
            cur.execute("SELECT preco FROM produtos WHERE id = ?", (item.produto_id,))
            preco = cur.fetchone()[0]

            # Insere o produto no carrinho
            cur.execute("""
                INSERT INTO carrinhos_produtos (carrinho_id, produto_id, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """, (carrinho_id, item.produto_id, item.quantidade, preco))

        con.commit()
        return {"mensagem": "Produto adicionado ao carrinho", "carrinho_id": carrinho_id}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.delete("/carrinho")
def remover_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()
    try:
        # Pega o carrinho do usuário
        cur.execute("SELECT id FROM carrinhos WHERE conta_id = ?", (item.usuario_id,))
        carrinho = cur.fetchone()
        if not carrinho:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")

        carrinho_id = carrinho[0]

        # Remove o produto
        cur.execute("""
            DELETE FROM carrinhos_produtos
            WHERE carrinho_id = ? AND produto_id = ?
        """, (carrinho_id, item.produto_id))

        con.commit()
        return {"mensagem": "Produto removido do carrinho"}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)