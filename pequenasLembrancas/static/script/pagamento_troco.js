const trocoInput = document.querySelector('#troco');
const trocoValor = document.querySelector('#troco-valor');

let valorNumerico = '';

trocoInput.addEventListener('keydown', function (evento) {

    // Permite teclas de controle
    if (
        evento.key === 'Tab' ||
        evento.key === 'ArrowLeft' ||
        evento.key === 'ArrowRight'
    ) {
        return;
    }

    // Backspace
    if (evento.key === 'Backspace') {

        evento.preventDefault();

        valorNumerico = valorNumerico.slice(0, -1);

        atualizarTroco();

        return;
    }

    // Delete
    if (evento.key === 'Delete') {

        evento.preventDefault();

        valorNumerico = '';

        atualizarTroco();

        return;
    }

    // Aceita somente números
    if (/^\d$/.test(evento.key)) {

        evento.preventDefault();

        valorNumerico += evento.key;

        atualizarTroco();

        return;
    }

    // Impede outros caracteres
    evento.preventDefault();
});


function atualizarTroco() {

    if (valorNumerico === '') {

        trocoInput.value = '';
        trocoValor.value = '';

        return;
    }

    const valor = Number(valorNumerico);

    // Valor enviado para o Flask
    trocoValor.value = valor.toFixed(2);

    // Valor mostrado para o cliente
    trocoInput.value = valor.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}