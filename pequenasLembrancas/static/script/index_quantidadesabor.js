document.querySelectorAll(".checkbox-sabor").forEach(function(checkbox) {

    checkbox.addEventListener("change", function() {

        const label = this.closest("label");

        const contador = label.querySelector(
            ".contador-addremove-sabores"
        );

        const quantidade = label.querySelector(
            ".quantidade-sabores"
        );


        if (this.checked) {

            quantidade.value = 1;
            contador.style.display = "flex";

        } else {

            quantidade.value = 0;
            contador.style.display = "none";

        }


        atualizarCaixinha();

    });

});



document.querySelectorAll(".btn-menos").forEach(function(botao) {

    botao.addEventListener("click", function(event) {

        event.preventDefault();

        const label = this.closest("label");

        const quantidade = label.querySelector(
            ".quantidade-sabores"
        );

        let valor = Number(quantidade.value);


        if (valor > 1) {

            valor--;

            quantidade.value = valor;

        }


        atualizarCaixinha();

    });

});



document.querySelectorAll(".btn-mais").forEach(function(botao) {

    botao.addEventListener("click", function(event) {

        event.preventDefault();

        const label = this.closest("label");

        const quantidade = label.querySelector(
            ".quantidade-sabores"
        );

        let valor = Number(quantidade.value);


        // Calcula a soma de todos os sabores
        let total = 0;

        document.querySelectorAll(".quantidade-sabores").forEach(function(input) {

            total += Number(input.value);

        });


        // Só permite aumentar se ainda não chegou a 4
        if (total < 4) {

            valor++;

            quantidade.value = valor;

        }


        atualizarCaixinha();

    });

});