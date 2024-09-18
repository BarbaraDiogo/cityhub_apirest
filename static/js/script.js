document.addEventListener('DOMContentLoaded', function() {
    // Extrai o número da porcentagem do texto do elemento h3
    const porcentagemText = document.getElementById('porcentagem').innerText;
    const porcentagem = parseInt(porcentagemText.match(/\d+/)); // Garante que apenas números sejam capturados

    console.log('Porcentagem:', porcentagem); // Isso mostrará o valor no console do navegador

    if (!isNaN(porcentagem)) {
        updateBarraProgresso(porcentagem);
    } else {
        console.error('Porcentagem não é um número válido:', porcentagemText);
    }
});

// Função para atualizar a largura da barra de progresso
function updateBarraProgresso(porcentagem) {
    console.log('Atualizando largura da barra para:', porcentagem + '%');
    document.getElementById('BarraProgresso').style.width = porcentagem + '%';
};

function confirmarDelecao(element) {
    if (confirm('Tem certeza que deseja deletar sua conta?')) {
        window.location.href = element.getAttribute('data-url');
    }
}
