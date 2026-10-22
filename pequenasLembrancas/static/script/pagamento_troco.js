const trocoInput = document.querySelector('#troco');
const trocoValor = document.querySelector('#troco-valor');
const formPagamento = trocoInput.form;
let digitos = '';

trocoInput.addEventListener('keydown', function (evento) {
    if ((evento.ctrlKey || evento.metaKey) && ['a', 'c', 'v'].includes(evento.key.toLowerCase())) {
        return;
    }

    if (evento.key === 'Tab' || evento.key.startsWith('Arrow')) {
        return;
    }

    if (/^\d$/.test(evento.key)) {
        evento.preventDefault();
        if (trocoInput.selectionStart === 0 && trocoInput.selectionEnd === trocoInput.value.length) {
            digitos = '';
        }
        digitos += evento.key;
        atualizarTroco();
        return;
    }

    if (evento.key === ',' || evento.key === '.') {
        evento.preventDefault();
        return;
    }

    if (evento.key === 'Backspace') {
        evento.preventDefault();
        if (trocoInput.selectionStart === 0 && trocoInput.selectionEnd === trocoInput.value.length) {
            digitos = '';
        } else {
            digitos = digitos.slice(0, -1);
        }
        atualizarTroco();
        return;
    }

    if (evento.key === 'Delete') {
        evento.preventDefault();
        digitos = '';
        atualizarTroco();
        return;
    }

    evento.preventDefault();
});

trocoInput.addEventListener('paste', function (evento) {
    evento.preventDefault();
    const textoColado = evento.clipboardData.getData('text');
    const valor = converterValor(textoColado);

    if (valor === null) {
        trocoInput.setCustomValidity('Informe um valor válido, por exemplo 50,00.');
        return;
    }

    digitos = String(Math.round(valor * 100));
    atualizarTroco();
});

formPagamento.addEventListener('submit', function () {
    atualizarTroco();
});

document.querySelectorAll('input[name="pagamento"]').forEach(function (opcao) {
    opcao.addEventListener('change', function () {
        if (opcao.value !== 'dinheiro') {
            digitos = '';
        }
    });
});

function converterValor(texto) {
    const valorLimpo = texto.trim().replace(/R\$\s?/gi, '').replace(/\s/g, '');
    if (!/^[\d.,]+$/.test(valorLimpo)) {
        return null;
    }

    const ultimaVirgula = valorLimpo.lastIndexOf(',');
    const ultimoPonto = valorLimpo.lastIndexOf('.');
    let parteInteira;
    let centavos = '';

    if (ultimaVirgula !== -1 && ultimoPonto !== -1) {
        const separadorDecimal = Math.max(ultimaVirgula, ultimoPonto);
        parteInteira = valorLimpo.slice(0, separadorDecimal).replace(/[.,]/g, '');
        centavos = valorLimpo.slice(separadorDecimal + 1);
    } else if (ultimaVirgula !== -1) {
        parteInteira = valorLimpo.slice(0, ultimaVirgula).replace(/,/g, '');
        centavos = valorLimpo.slice(ultimaVirgula + 1);
    } else if (ultimoPonto !== -1 && !/^\d{1,3}(?:\.\d{3})+$/.test(valorLimpo)) {
        parteInteira = valorLimpo.slice(0, ultimoPonto).replace(/\./g, '');
        centavos = valorLimpo.slice(ultimoPonto + 1);
    } else {
        parteInteira = valorLimpo.replace(/[.,]/g, '');
    }

    if ((!parteInteira && !centavos) || centavos.length > 2) {
        return null;
    }

    const valor = Number(`${parteInteira || '0'}.${centavos.padEnd(2, '0')}`);
    return Number.isFinite(valor) ? valor : null;
}

function atualizarTroco() {
    if (!digitos) {
        trocoInput.value = '';
        trocoValor.value = '';
        trocoInput.setCustomValidity('');
        return;
    }

    const valor = Number(digitos) / 100;

    if (!Number.isFinite(valor)) {
        trocoInput.setCustomValidity('Informe um valor válido, por exemplo 50,00.');
        return;
    }

    trocoInput.setCustomValidity('');
    trocoValor.value = valor.toFixed(2);
    trocoInput.value = valor.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}