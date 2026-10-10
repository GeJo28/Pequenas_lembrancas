const checkboxes = document.querySelectorAll(".checkbox-sabor");
const botao = document.getElementById("botao-adicionar");

checkboxes.forEach(function(checkbox) {

    checkbox.addEventListener("change", function() {

        const selecionados =
            document.querySelectorAll(".checkbox-sabor:checked");

        botao.disabled = selecionados.length !== 4;

    });

});