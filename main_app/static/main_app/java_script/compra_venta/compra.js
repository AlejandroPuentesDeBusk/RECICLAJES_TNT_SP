document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.cajita');
    const listaMaterialesSeleccionados = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo'); // Select para tipo de precio

    // Función para obtener el precio según la selección en el <select>
    function obtenerPrecio(materialCheckbox) {
        return tipoCargoSelect.value === "Wholesale_Purchase_Price" 
               ? materialCheckbox.getAttribute('data-wholesale_purchase_price')
               : materialCheckbox.getAttribute('data-retail_purchase_price');
    }

    // Función para actualizar la lista de materiales seleccionados
    function actualizarMaterialSeleccionado(checkbox) {
        const material = checkbox.getAttribute('data-material');
        const price = obtenerPrecio(checkbox);

        // Crear o actualizar el elemento de lista
        let listItem = listaMaterialesSeleccionados.querySelector(`li[data-material="${material}"]`);
        
        if (checkbox.checked) {
            if (!listItem) {
                listItem = document.createElement('li');
                listItem.setAttribute('data-material', material);
                listaMaterialesSeleccionados.appendChild(listItem);
            }
            listItem.innerHTML = `<span><strong>Material:</strong> ${material}</span> 
                                  <span><strong>Precio:</strong> ${price}</span>`;
        } else {
            if (listItem) {
                listaMaterialesSeleccionados.removeChild(listItem);
            }
        }
    }

    // Añadir evento 'change' a cada checkbox
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            actualizarMaterialSeleccionado(checkbox);
        });
    });

    // Evento para actualizar los precios cuando se cambia el tipo de precio en el <select>
    tipoCargoSelect.addEventListener('change', function () {
        checkboxes.forEach((checkbox) => {
            // Si el material está seleccionado, actualizar el precio mostrado
            if (checkbox.checked) {
                actualizarMaterialSeleccionado(checkbox);
            }
        });
    });
});



