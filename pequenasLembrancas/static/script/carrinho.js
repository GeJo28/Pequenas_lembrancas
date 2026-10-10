const inputs = document.querySelectorAll(".contador-addremove input");

inputs.forEach(function(input) {

    input.addEventListener("input", function() {

        const quantidade = input.value.length;

        input.style.width = (20 + quantidade * 10) + "px";

    });

});