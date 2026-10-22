const abrirModal = document.getElementById("abrir-modal");
const fecharModal = document.getElementById("fechar-modal");
const modal = document.getElementById("modal");
const tituloModal = document.getElementById("modal-titulo");

function abrirSelecaoSabores() {
    modal.style.display = "flex";
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-aberto");
    fecharModal.focus();
}

function fecharSelecaoSabores() {
    modal.style.display = "none";
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-aberto");
    abrirModal.focus();
}

abrirModal.addEventListener("click", abrirSelecaoSabores);
fecharModal.addEventListener("click", fecharSelecaoSabores);

modal.addEventListener("click", function(evento) {
    if (evento.target === modal) {
        fecharSelecaoSabores();
    }
});

modal.addEventListener("keydown", function(evento) {
    if (evento.key === "Escape") {
        evento.preventDefault();
        fecharSelecaoSabores();
        return;
    }

    if (evento.key !== "Tab") {
        return;
    }

    const elementosFocaveis = Array.from(
        modal.querySelectorAll('button:not(:disabled), input:not(:disabled), [href], [tabindex]:not([tabindex="-1"])')
    ).filter((elemento) => elemento.getClientRects().length > 0);

    if (elementosFocaveis.length === 0) {
        evento.preventDefault();
        tituloModal.focus();
        return;
    }

    const primeiro = elementosFocaveis[0];
    const ultimo = elementosFocaveis[elementosFocaveis.length - 1];

    if (evento.shiftKey && document.activeElement === primeiro) {
        evento.preventDefault();
        ultimo.focus();
    } else if (!evento.shiftKey && document.activeElement === ultimo) {
        evento.preventDefault();
        primeiro.focus();
    }
});