async function atualizarContadorCarrinho() {
    try {
        const response = await fetch('/carrinho');
        const data = await response.json();
        
        const totalItens = data.produtos ? data.produtos.length : 0;
        
        const badge = document.getElementById('cart-count');
        if (badge) {
            badge.textContent = totalItens;
            badge.style.display = totalItens > 0 ? 'inline' : 'none';
        }
    } catch (error) {
        console.error('Erro ao atualizar contador:', error);
    }
}

// Atualiza ao carregar a página
document.addEventListener('DOMContentLoaded', atualizarContadorCarrinho);

function formatPrice(price) {
    return price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}


function createProductCard(product) {
    return `
        <div class="product-card"
             onclick="window.location.href='produto.html?id=${product.id}'">
            <img src="${product.imagem}" alt="${product.nome}" class="product-image">
            <h3 class="product-title">${product.nome}</h3>
            <div class="product-price">${formatPrice(product.preco)}</div>
        </div>
    `
}

async function renderProduct() {
    const grid = document.getElementById('productsGrid')
    try {
        const resposta = await fetch('http://127.0.0.1:8000/produtos');
        const produtos = await resposta.json();
        grid.innerHTML = produtos.map(createProductCard).join('')


    } catch (err) {
        console.error('Erro ao carregar produtos:', err);
    }
}

function searchProducts(){
   const searchInput = document.getElementById('searchInput').value.toLowerCase()

   const filteredProducts = products.filter(product => product.title.toLowerCase().includes(searchInput))

    renderProduct()
}

renderProduct()

document.getElementById('searchBtn').addEventListener('click', searchProducts)
// addEventListener -> escutador de eventos. Vai ficar esperando o evento click acontecer
