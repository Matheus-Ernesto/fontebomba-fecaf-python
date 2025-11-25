let produtoAtual = null;

function formatPrice(price) {
  return price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

async function carregarProduto() {
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));

  const container = document.getElementById('productDetail');

  if (!id) {
    container.innerHTML = "<p>Produto não encontrado.</p>";
    return;
  }

  try {
    // pega todos os produtos e filtra pelo id
    const resp = await fetch('http://127.0.0.1:8000/produtos');
    const produtos = await resp.json();

    const produto = produtos.find(p => p.id === id);

    if (!produto) {
      container.innerHTML = "<p>Produto não encontrado.</p>";
      return;
    }

    // guarda pra usar depois no "Adicionar ao carrinho"
    produtoAtual = produto;

    container.innerHTML = `
      <div class="product-detail">
        <img src="${produto.imagem}" alt="${produto.nome}" class="product-image">
        <h1>${produto.nome}</h1>
        <p class="product-price">${formatPrice(produto.preco)}</p>
        <p>${produto.descricao || ''}</p>
        <p>Estoque: ${produto.estoque}</p>

        <div style="margin-top: 20px; display: flex; gap: 10px;">
          <button id="btnAddCart">Adicionar ao carrinho</button>
          <button onclick="window.location.href='index.html'">Voltar</button>
        </div>
      </div>
    `;

    // liga o botão depois que o HTML foi inserido
    document
      .getElementById('btnAddCart')
      .addEventListener('click', adicionarAoCarrinho);

  } catch (err) {
    console.error(err);
    container.innerHTML = "<p>Erro ao carregar produto.</p>";
  }
}

async function adicionarAoCarrinho() {
  if (!produtoAtual) return;

  const usuarioId = Number(localStorage.getItem('usuario_id'));

  // se não estiver logado, manda pro login
  if (!usuarioId) {
    alert('Você precisa estar logado para adicionar ao carrinho.');
    window.location.href = 'login.html';
    return;
  }

  try {
    const resp = await fetch('http://127.0.0.1:8000/carrinho', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        usuario_id: usuarioId,
        produto_id: produtoAtual.id,
        quantidade: 1
      })
    });

    const data = await resp.json();

    if (!resp.ok) {
      throw new Error(data.detail || 'Erro ao adicionar ao carrinho');
    }

    // ✅ MUDANÇAS AQUI: remove o alert e adiciona feedback melhor
    await atualizarContadorCarrinho();
    mostrarNotificacao('✅ Produto adicionado ao carrinho!');
    
  } catch (err) {
    console.error(err);
    alert('Erro ao adicionar ao carrinho.');
  }
}


async function atualizarContadorCarrinho() {
  try {
    const usuarioId = Number(localStorage.getItem('usuario_id'));
    if (!usuarioId) return;

    const response = await fetch(`http://127.0.0.1:8000/carrinho?usuario_id=${usuarioId}`);
    const data = await response.json();
    
    const totalItens = data.itens ? data.itens.length : 0;
    
    const badge = document.getElementById('cart-count');
    if (badge) {
      badge.textContent = totalItens;
      badge.style.display = totalItens > 0 ? 'inline' : 'none';
    }
  } catch (error) {
    console.error('Erro ao atualizar contador:', error);
  }
}

function mostrarNotificacao(mensagem) {
  const notif = document.createElement('div');
  notif.textContent = mensagem;
  notif.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #4CAF50;
    color: white;
    padding: 15px 25px;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 9999;
    animation: slideIn 0.3s ease-out;
  `;
  document.body.appendChild(notif);
  
  setTimeout(() => {
    notif.style.animation = 'slideOut 0.3s ease-in';
    setTimeout(() => notif.remove(), 300);
  }, 3000);
}

// Atualiza o contador quando a página carregar
document.addEventListener('DOMContentLoaded', atualizarContadorCarrinho);

carregarProduto();
