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
    cur.execute("SELECT id, nome, preco, descricao, estoque, imagem FROM produtos")
    dados = cur.fetchall()
    con.close()
    return [
        {"id": d[0], "nome": d[1], "preco": d[2], "descricao": d[3], "estoque": d[4], "imagem": d[5]}
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

    cur.execute("""
        SELECT ci.produto_id, p.nome, ci.preco, ci.quantidade, p.imagem
        FROM carrinho_itens ci
        JOIN produtos p ON ci.produto_id = p.id
        WHERE ci.conta_id = ?
    """, (usuario_id,))

    itens = cur.fetchall()
    con.close()

    if not itens:
        return {"mensagem": "Carrinho vazio", "itens": []}

    total = sum(i[2] * i[3] for i in itens)

    return {
        "total": total,
        "itens": [
            {"produto_id": i[0], "nome": i[1], "preco": i[2], "quantidade": i[3], "imagem": i[4]}
            for i in itens
        ]
    }


@app.post("/carrinho")
def adicionar_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()
    try:
        # Verifica se o item já existe no carrinho
        cur.execute("""
            SELECT quantidade FROM carrinho_itens
            WHERE conta_id = ? AND produto_id = ?
        """, (item.usuario_id, item.produto_id))
        existente = cur.fetchone()

        if existente:
            nova_qtde = existente[0] + item.quantidade
            cur.execute("""
                UPDATE carrinho_itens
                SET quantidade = ?
                WHERE conta_id = ? AND produto_id = ?
            """, (nova_qtde, item.usuario_id, item.produto_id))
        else:
            # Obtém o preço atual
            cur.execute("SELECT preco FROM produtos WHERE id = ?", (item.produto_id,))
            preco = cur.fetchone()
            if not preco:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            preco = preco[0]

            # Insere no carrinho
            cur.execute("""
                INSERT INTO carrinho_itens (conta_id, produto_id, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """, (item.usuario_id, item.produto_id, item.quantidade, preco))

        con.commit()
        return {"mensagem": "Produto adicionado ao carrinho!"}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.delete("/carrinho")
def remover_carrinho(item: CarrinhoItem):
    con = conectar()
    cur = con.cursor()

    try:
        # 1. Buscar quantidade atual
        cur.execute("""
            SELECT quantidade FROM carrinho_itens
            WHERE conta_id = ? AND produto_id = ?
        """, (item.usuario_id, item.produto_id))

        resultado = cur.fetchone()

        if not resultado:
            raise HTTPException(status_code=404, detail="Item não está no carrinho!")

        quantidade_atual = resultado[0]

        # 2. Se quantidade > 1 → diminuir
        if quantidade_atual > 1:
            cur.execute("""
                UPDATE carrinho_itens
                SET quantidade = quantidade - 1
                WHERE conta_id = ? AND produto_id = ?
            """, (item.usuario_id, item.produto_id))

            con.commit()
            return {"mensagem": "Quantidade reduzida!"}

        # 3. Se quantidade == 1 → remover item
        cur.execute("""
            DELETE FROM carrinho_itens
            WHERE conta_id = ? AND produto_id = ?
        """, (item.usuario_id, item.produto_id))

        con.commit()
        return {"mensagem": "Item removido do carrinho!"}

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