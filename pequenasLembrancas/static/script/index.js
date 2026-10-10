const abrirModal = document.getElementById("abrir-modal");
const fecharModal = document.getElementById("botao-adicionar");
const modal = document.getElementById("modal");

abrirModal.addEventListener("click", function(){
    modal.style.display = "flex";
})

fecharModal.addEventListener("click", function(){
    modal.style.display = "none";
})

modal.addEventListener("click", function(){
    if(event.target === modal){
        modal.style.display = "none";
    }
})