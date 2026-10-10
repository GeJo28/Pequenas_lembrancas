const celular = document.getElementById("celular");
const form = document.getElementById("form-entrega");


// Formata o celular enquanto o usuário digita
celular.addEventListener("input", function () {

    let numero = celular.value.replace(/\D/g, "");

    numero = numero.substring(0, 11);

    if (numero.length <= 2) {

        celular.value = `(${numero}`;

    } else if (numero.length <= 7) {

        celular.value =
            `(${numero.substring(0, 2)}) ${numero.substring(2)}`;

    } else {

        celular.value =
            `(${numero.substring(0, 2)}) ${numero.substring(2, 7)}-${numero.substring(7)}`;

    }

});


// Remove a formatação antes de enviar para o Flask
form.addEventListener("submit", function () {

    celular.value = celular.value.replace(/\D/g, "");

});