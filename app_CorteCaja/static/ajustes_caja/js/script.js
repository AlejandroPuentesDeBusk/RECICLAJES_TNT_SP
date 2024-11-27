document.addEventListener("DOMContentLoaded", () => {
    const montoInput = document.getElementById("monto");
    const tipoOperacion = document.getElementById("tipo_operacion");
    const submitButton = document.getElementById("realizar_compra");

    montoInput.addEventListener("input", () => {
        const monto = parseFloat(montoInput.value) || 0;

        // Validar si es un gasto y excede el dinero en caja
        if (tipoOperacion.value === "EXPENSE" && monto > dineroEnCaja) {
            submitButton.disabled = true;
        } else {
            submitButton.disabled = false;
        }
    });
});

