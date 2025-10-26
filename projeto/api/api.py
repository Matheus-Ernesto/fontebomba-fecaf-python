from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# Cria a app FastAPI
app = FastAPI()

# Configuração do CORS (libera o acesso do front-end)
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
# MODELO PARA LOGIN
# -----------------------------
class Login(BaseModel):
    email: str
    senha: str

# Modelo para atualização de email
class AtualizarEmail(BaseModel):
    id: int
    novo_email: str

# Modelo para atualização de senha
class AtualizarSenha(BaseModel):
    id: int
    nova_senha: str

# Modelo para adicionar/remover produto do carrinho
class CarrinhoItem(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int = 1


# -----------------------------
# ROTAS
# -----------------------------
@app.get("/")
def home():
    return {"mensagem": "API da Loja funcionando!"}

@app.get("/produtos")
def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM produtos")
    dados = cur.fetchall()
    con.close()
    return [
        {"id": d[0], "nome": d[1], "preco": d[2], "estoque": d[3]}
        for d in dados
    ]

@app.get("/contas")
def listar_contas():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, email FROM contas")
    dados = cur.fetchall()
    con.close()
    return [
        {"id": d[0], "nome": d[1], "email": d[2]}
        for d in dados
    ]

# -----------------------------
# LOGIN
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

@app.get("/carrinho/{usuario_id}")
def listar_carrinho(usuario_id: int):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT c.produto_id, p.nome, p.preco, c.quantidade
        FROM carrinhos c
        JOIN produtos p ON c.produto_id = p.id
        WHERE c.usuario_id = ?
    """, (usuario_id,))
    itens = cur.fetchall()
    con.close()
    return [
        {"produto_id": i[0], "nome": i[1], "preco": i[2], "quantidade": i[3]}
        for i in itens
    ]

@app.post("/carrinho")
def adicionar_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()
    try:
        # Verifica se já existe o item no carrinho
        cur.execute("SELECT quantidade FROM carrinhos WHERE usuario_id = ? AND produto_id = ?",
                    (item.usuario_id, item.produto_id))
        existente = cur.fetchone()
        if existente:
            nova_qtde = existente[0] + item.quantidade
            cur.execute("UPDATE carrinhos SET quantidade = ? WHERE usuario_id = ? AND produto_id = ?",
                        (nova_qtde, item.usuario_id, item.produto_id))
        else:
            cur.execute("INSERT INTO carrinhos (usuario_id, produto_id, quantidade) VALUES (?, ?, ?)",
                        (item.usuario_id, item.produto_id, item.quantidade))
        con.commit()
        return {"mensagem": "Produto adicionado ao carrinho"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.delete("/carrinho")
def remover_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM carrinhos WHERE usuario_id = ? AND produto_id = ?",
                    (item.usuario_id, item.produto_id))
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