# Projeto Loja Funcional

Este projeto é um **exemplo de loja funcional** desenvolvido como **trabalho da disciplina de Desenvolvimento em Python**, ministrada pelo professor **Daniel Xavier**.

Alunos:

- Daniel Sanjines Lozano.
- Diego Gonçalves dos Santos.
- Guilherme Souza.
- Henrique Luiz Ramos.
- João Arnaldo Mariano.
- Matheus Ernesto dos Santos. - RA: 43202
- Pedro Ribeiro.


O projeto utiliza:

- **Banco de dados relacional:** SQLite
- **API:** FastAPI para fornecer requisições RESTful em JSON
- **Front-end Web:** HTML + Tailwind CSS

---

## Estrutura do Projeto

projeto

|

├─ api/ → Código da API (FastAPI)

├─ bd/ → Scripts para criação e inserção no banco SQLite

└─ web/ → Páginas Web (index, login, conta, carrinho, compra)


---

## Funcionalidades

- **Index:** Página principal exibindo produtos
- **Login:** Autenticação de usuários
- **Conta:** Alterar email e senha do usuário
- **Carrinho:** Visualizar, adicionar e remover produtos
- **Compra:** Simulação de finalização de pedidos

---

## Observações

- A API deve estar rodando para que o front-end funcione corretamente.
- O banco SQLite (`.db`) está localizado na pasta `bd/`.

---

## Como rodar

- Para executar o servidor, rode o `uvicorn api:app --reload` dentro da pasta api.
- abra a pagina desejada no navegador de sua preferência (a página inicial é o index.html).
- Bom uso!
