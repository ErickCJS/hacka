document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("formDenuncia");
    const alerta = document.getElementById("alerta");

    function validarFormulario() {

        const campos = ["numero_placa", "color", "tipo", "telefono"];

        let valido = true;

        campos.forEach(campo => {

            const input = form[campo];

            if (!input) return;

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

        // Mostrar alerta animada
        alerta.classList.remove("d-none");
        alerta.classList.add("show");

        alerta.style.opacity = "0";
        setTimeout(() => {
            alerta.style.transition = "opacity .4s ease";
            alerta.style.opacity = "1";
        }, 50);

        // Resetear formulario
        form.reset();

        // Ocultar alerta suave
        setTimeout(() => {
            alerta.style.opacity = "0";
            setTimeout(() => alerta.classList.add("d-none"), 400);
        }, 4000);
    });

});
