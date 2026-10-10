const quantidadeCoxinha = document.querySelector("#quantidade-coxinha");
const botaoMaisCoxinha = document.querySelector(".btn-mais-coxinha");
const botaoMenosCoxinha = document.querySelector(".btn-menos-coxinha");
const botaoAdicionarCoxinha = document.querySelector(".botao-coxinha");

function atualizarBotaoCoxinha() {
    if (parseInt(quantidadeCoxinha.value) >= 1) {
        botaoAdicionarCoxinha.disabled = false;
    } else {
        botaoAdicionarCoxinha.disabled = true;
    }
}

botaoMaisCoxinha.addEventListener("click", function() {
    quantidadeCoxinha.value = parseInt(quantidadeCoxinha.value) + 1;
    atualizarBotaoCoxinha();
});

botaoMenosCoxinha.addEventListener("click", function() {
    let valor = parseInt(quantidadeCoxinha.value);

    if (valor > 0) {
        quantidadeCoxinha.value = valor - 1;
    }

    atualizarBotaoCoxinha();
});

// NOVO: atualiza o botão quando o usuário digitar no input
quantidadeCoxinha.addEventListener("input", function() {
    atualizarBotaoCoxinha();
});

atualizarBotaoCoxinha();