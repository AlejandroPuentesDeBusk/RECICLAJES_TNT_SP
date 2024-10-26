// Obtener los elementos del DOM
const modal1 = document.getElementById("modal1");
const modal2 = document.getElementById("modal2");
const abrir_modal = document.getElementById("boton_modal");
const cerrar_modal = document.getElementById("cerrar_vent_modal");
const confirmar_compra = document.getElementById("confirmar");
const regresar = document.getElementById("boton_regresar");

// Función para abrir el primer modal de compra/venta
abrir_modal.addEventListener("click", () => {
    modal1.style.display = "flex";
});

// Función para cerrar el primer modal
cerrar_modal.addEventListener("click", () => {
    modal1.style.display = "none";
});

// Función para abrir el segundo modal al confirmar la compra/venta
confirmar_compra.addEventListener("click", () => {
    modal1.style.display = "none";
    modal2.style.display = "flex";
});

// Función para cerrar el segundo modal (al presionar "Regresar" te lleva atras)
regresar.addEventListener("click", () => {
    modal2.style.display = "none";
});
