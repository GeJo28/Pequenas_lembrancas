const inputs = document.querySelectorAll(".contador-addremove input");

const checkboxes = document.querySelectorAll(".checkbox-sabor");

const quantidade = document.querySelector("#quantidade");

const botaoAdicionar = document.querySelector("#botao-adicionar");

// ACRESCENTADO: seleciona os botões do contador de caixinhas
const botaoMenosCaixinha = document.querySelector(
    ".contador-addremove button:first-child"
);

const botaoMaisCaixinha = document.querySelector(
    ".contador-addremove button:last-child"
);


inputs.forEach(function(input) {

    input.addEventListener("input", function() {

        const quantidade = input.value.length;

        input.style.width = (20 + quantidade * 10) + "px";

    });

});


checkboxes.forEach(function(checkbox) {

    checkbox.addEventListener("change", function() {

        atualizarCaixinha();

    });

});


const quantidadesSabores = document.querySelectorAll(".quantidade-sabores");


function atualizarCaixinha() {

    let total = 0;


    // Soma a quantidade de todos os sabores
    quantidadesSabores.forEach(function(input) {

        total += Number(input.value);

    });


    // LIMITA O TOTAL DE BRIGADEIROS A 4
    checkboxes.forEach(function(checkbox) {

        if (total >= 4 && !checkbox.checked) {

            checkbox.disabled = true;

        } else {

            checkbox.disabled = false;

        }

    });


    // CONTROLA A CAIXINHA
    if (total === 4) {

        quantidade.value = 1;

        // ACRESCENTADO: libera o input para digitação
        quantidade.readOnly = false;

        // ACRESCENTADO: habilita os botões
        botaoMenosCaixinha.disabled = false;
        botaoMaisCaixinha.disabled = false;

        botaoAdicionar.disabled = false;

    } else {

        quantidade.value = 0;

        // ACRESCENTADO: bloqueia a digitação
        quantidade.readOnly = true;

        // ACRESCENTADO: desabilita os botões
        botaoMenosCaixinha.disabled = true;
        botaoMaisCaixinha.disabled = true;

        botaoAdicionar.disabled = true;

    }

}


// Botão de diminuir a quantidade de caixinhas
botaoMenosCaixinha.addEventListener("click", function(event) {

    event.preventDefault();

    let valor = Number(quantidade.value);

    if (valor > 1) {

        valor--;

        quantidade.value = valor;

    }

});


// Botão de aumentar a quantidade de caixinhas
botaoMaisCaixinha.addEventListener("click", function(event) {

    event.preventDefault();

    let valor = Number(quantidade.value);

    valor++;

    quantidade.value = valor;

});


// ACRESCENTADO: controla o valor digitado manualmente
quantidade.addEventListener("input", function() {

    // Permite apagar o conteúdo temporariamente
    if (quantidade.value === "") {
        return;
    }

    let valor = Number(quantidade.value);

    // Impede valores negativos e decimais
    if (!Number.isInteger(valor) || valor < 1) {
        quantidade.value = "";
    }

});

// ACRESCENTADO: configura o estado inicial
quantidade.readOnly = true;

botaoMenosCaixinha.disabled = true;
botaoMaisCaixinha.disabled = true;

atualizarCaixinha();