const form = document.getElementById("formDenuncia");
const alerta = document.getElementById("alerta");

// Validación rápida
function validarFormulario() {
    const campos = ["nombre", "correo", "telefono", "tipo", "descripcion"];
    let valido = true;

    campos.forEach(campo => {
        const input = form[campo];

        if (!input.value.trim()) {
            input.classList.add("is-invalid");
            valido = false;
        } else {
            input.classList.remove("is-invalid");
        }
    });

    return valido;
}

form.addEventListener("submit", (e) => {
    e.preventDefault();

    if (!validarFormulario()) {
        return;
    }

    // Mostrar alerta elegante
    alerta.classList.remove("d-none");
    alerta.classList.add("show");

    // Animación suave
    alerta.style.opacity = "0";
    setTimeout(() => {
        alerta.style.transition = "opacity .4s ease";
        alerta.style.opacity = "1";
    }, 50);

    // Limpiar formulario
    form.reset();

    // Ocultar alerta después de 4 segundos
    setTimeout(() => {
        alerta.style.opacity = "0";
        setTimeout(() => alerta.classList.add("d-none"), 400);
    }, 4000);
});
