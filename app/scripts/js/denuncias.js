const form = document.getElementById("formDenuncia");
const alerta = document.getElementById("alerta");

form.addEventListener("submit", (e) => {
    e.preventDefault();

    alerta.classList.remove("d-none");
    alerta.classList.add("show");

    form.reset();
});
