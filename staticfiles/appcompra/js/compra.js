document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.cajita');
    const lista_Material = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo');
    const tipoOperacionSelect = document.getElementById('tipo_operacion'); // Nuevo select para tipo de operación
    const total_final = document.getElementById('total_general');
    const discount_int = document.getElementById('discount');
    const extra_charge_int = document.getElementById('extra_charge');
    const realizarCompraBtn = document.getElementById('realizar_compra');


    // Obtener el precio según operación (compra/venta) y tipo de cargo (mayoreo/menudeo)
    function obtenerPrecio(materialCheckbox) {
        const operacion = tipoOperacionSelect.value; // "compra" o "venta"
        const tipoCargo = tipoCargoSelect.value; // "Wholesale_Purchase_Price", "Retail_Purchase_Price", etc.

        if (operacion === "compra") {
            return tipoCargo === "Wholesale_Purchase_Price"
                ? materialCheckbox.getAttribute('data-wholesale_purchase_price')
                : materialCheckbox.getAttribute('data-retail_purchase_price');
        } else if (operacion === "venta") {
            return tipoCargo === "Wholesale_Purchase_Price"
                ? materialCheckbox.getAttribute('data-wholesale_sale_price')
                : materialCheckbox.getAttribute('data-retail_sale_price');
        }
    }

    function actualizar_total() {
        let total_general = 0;

        lista_Material.querySelectorAll('.precio_total').forEach(span => {
            total_general += parseFloat(span.textContent) || 0;
        });

        const discount = parseFloat(discount_int.value) || 0;
        const extra_charge = parseFloat(extra_charge_int.value) || 0;

        const total_modified = total_general - discount + extra_charge;

        total_final.textContent = `${total_modified.toFixed(2)} MXN`;
    }




    function actualizarMaterialSeleccionado(checkbox) {
        const material = checkbox.getAttribute('data-material');
        const price = obtenerPrecio(checkbox);
        const image = checkbox.getAttribute('data-image');
    
        // Verifica si el material ya está en la lista
        let listItem = lista_Material.querySelector(`li[data-material="${material}"]`);
        let hrElement = lista_Material.querySelector(`hr[data-material-hr="${material}"]`); // Identifica el <hr> relacionado
    
        if (checkbox.checked) {
            if (!listItem) {
                // Crear el elemento de lista si no existe
                listItem = document.createElement('li');
                listItem.setAttribute('data-material', material);
                listItem.className = "list-item";
                lista_Material.appendChild(listItem);
    
                // Crear el <hr> si no existe
                hrElement = document.createElement('hr');
                hrElement.setAttribute('data-material-hr', material);
                lista_Material.appendChild(hrElement);
            }
            listItem.innerHTML = `<span> <strong> ${material}</strong></span> 
                                  <span><strong>Precio:</strong> ${price} </span>
                                  <span>
                                    <img src="${image}" alt="${material}" class="imagen">
                                  </span>
                                  <span>
                                    <input type="number" placeholder="cant(kg)" class="cant_total" required min="0" step="1">
                                  </span>
                                  <span><strong>Total:</strong> <span class="precio_total">0 MXN</span></span>`;
    
            const kg_input = listItem.querySelector('.cant_total');
            const precio_total = listItem.querySelector('.precio_total');
    
            kg_input.addEventListener('input', function () {
                const cantidad = parseFloat(kg_input.value) || 0;
                const total = (cantidad * price).toFixed(2);
                precio_total.textContent = `${total} MXN`;
                actualizar_total();
            });
    
        } else {
            // Eliminar el elemento y su <hr> relacionado si el checkbox se desmarca
            if (listItem) {
                lista_Material.removeChild(listItem);
            }
            if (hrElement) {
                lista_Material.removeChild(hrElement);
            }
            actualizar_total();
        }
    }
    










    // Actualizar los materiales seleccionados al cambiar la operación o el tipo de precio
    function actualizarTodosMateriales() {
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                actualizarMaterialSeleccionado(checkbox);
            }
        });
        actualizar_total();
    }

    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            actualizarMaterialSeleccionado(checkbox);
        });
    });

    tipoCargoSelect.addEventListener('change', actualizarTodosMateriales);
    tipoOperacionSelect.addEventListener('change', actualizarTodosMateriales); // Nuevo evento para el select de tipo_operacion
    discount_int.addEventListener('input', actualizar_total);
    extra_charge_int.addEventListener('input', actualizar_total);
});
