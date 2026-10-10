const opcoesPagamento = document.querySelectorAll(
    'input[name="pagamento"]'
);

const trocoDiv = document.querySelector(".troco-div");


opcoesPagamento.forEach((opcao) => {

    opcao.addEventListener("change", () => {

        if (opcao.value === "dinheiro") {

            trocoDiv.style.display = "block";

        } else {

            trocoDiv.style.display = "none";

            document.querySelector("#troco").value = "";
            document.querySelector("#troco-valor").value = "";

        }

    });

});