document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.cajita');
    const lista_Material = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo');
    const tipoOperacionSelect = document.getElementById('tipo_operacion');
    const total_final = document.getElementById('total_general');
    const discount_int = document.getElementById('discount');
    const extra_charge_int = document.getElementById('extra_charge');
    const realizar_compra_btn = document.getElementById('realizar_compra');

    let tipoOperacionSeleccionado = false; // Banderas para verificar interacción
    let tipoCargoSeleccionado = false;

    const selectedMaterialsKey = 'selectedMaterials'; // Clave global para almacenar la selección en localStorage
    let savedSelections = JSON.parse(localStorage.getItem(selectedMaterialsKey)) || [];

    // Validar si los selects han sido configurados manualmente
    function areSelectionsValid() {
        return tipoOperacionSeleccionado && tipoCargoSeleccionado;
    }

    // Mostrar un mensaje de error si no se han seleccionado los valores
    function showSelectionError() {
        alert("Por favor, selecciona el tipo de operación y el tipo de cargo antes de agregar materiales.");
    }

    // Manejar cambios en los selects
    tipoOperacionSelect.addEventListener('change', function () {
        tipoOperacionSeleccionado = true; // Marca que el usuario ha interactuado
    });

    tipoCargoSelect.addEventListener('change', function () {
        tipoCargoSeleccionado = true; // Marca que el usuario ha interactuado
    });

    // Manejar eventos de selección de los checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (!areSelectionsValid()) {
                showSelectionError();
                checkbox.checked = false; // Desmarcar el checkbox si no está permitido
                return;
            }

            const materialId = checkbox.getAttribute('data-material');
            const materialName = checkbox.getAttribute('data-material-name');
            const price = obtenerPrecio(checkbox);
            const image = checkbox.getAttribute('data-image');

            if (checkbox.checked) {
                const materialData = { materialId, materialName, price, image, cantidad: 0 };
                guardarSeleccion(materialData);
                actualizarMaterialEnCalculadora(materialData);
            } else {
                const listItem = lista_Material.querySelector(`li[data-material="${materialId}"]`);
                if (listItem) {
                    lista_Material.removeChild(listItem);
                }
                guardarSeleccion({ materialId, cantidad: 0 });
            }

            actualizar_total();
        });
    });

    function obtenerPrecio(checkbox) {
        const operacion = tipoOperacionSelect.value;
        const tipoCargo = tipoCargoSelect.value;
        return operacion === 'compra'
            ? parseFloat(checkbox.getAttribute(`data-${tipoCargo}`))
            : parseFloat(checkbox.getAttribute(`data-${tipoCargo.replace('Purchase', 'Sale')}`));
    }

    // Restaurar selección desde localStorage
    function restoreSelections() {
        lista_Material.innerHTML = '';

        savedSelections.forEach(savedItem => {
            const materialId = savedItem.materialId;
            const checkbox = document.querySelector(`.cajita[data-material="${materialId}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
            actualizarMaterialEnCalculadora(savedItem);
        });

        actualizar_total();
    }

    function guardarSeleccion(materialData) {
        const index = savedSelections.findIndex(item => item.materialId === materialData.materialId);

        if (materialData.cantidad > 0) {
            if (index > -1) {
                savedSelections[index] = materialData;
            } else {
                savedSelections.push(materialData);
            }
        } else if (index > -1) {
            savedSelections.splice(index, 1);
        }

        localStorage.setItem(selectedMaterialsKey, JSON.stringify(savedSelections));
    }

    function actualizarMaterialEnCalculadora(materialData) {
        const { materialId, materialName, price, image, cantidad } = materialData;

        let listItem = lista_Material.querySelector(`li[data-material="${materialId}"]`);
        if (!listItem) {
            listItem = document.createElement('li');
            listItem.setAttribute('data-material', materialId);
            lista_Material.appendChild(listItem);
        }

        listItem.innerHTML = `
            <strong>${materialName}</strong> - ${price} MXN
            ${image ? `<img src="${image}" class="imagen" alt="${materialName}">` : ''}
            <input type="number" class="cant_total" min="0" placeholder="Cantidad" value="${cantidad}">
            <span class="precio_total">${(cantidad * price).toFixed(2)}</span> MXN
        `;

        const inputCantidad = listItem.querySelector('.cant_total');
        inputCantidad.addEventListener('input', function () {
            const nuevaCantidad = parseFloat(this.value) || 0;
            listItem.querySelector('.precio_total').textContent = (nuevaCantidad * price).toFixed(2);

            const updatedMaterialData = { materialId, materialName, price, image, cantidad: nuevaCantidad };
            guardarSeleccion(updatedMaterialData);

            if (nuevaCantidad <= 0) {
                lista_Material.removeChild(listItem);
                const checkbox = document.querySelector(`.cajita[data-material="${materialId}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
            }

            actualizar_total();
        });
    }

    function actualizar_total() {
        let total_general = 0;
        lista_Material.querySelectorAll('.precio_total').forEach(span => {
            total_general += parseFloat(span.textContent) || 0;
        });

        const discount = parseFloat(discount_int.value) || 0;
        const extra_charge = parseFloat(extra_charge_int.value) || 0;
        const total_con_descuento = total_general - discount + extra_charge;
        total_final.textContent = `${total_con_descuento.toFixed(2)} MXN`;

        realizar_compra_btn.disabled = total_con_descuento <= 0;
    }

    restoreSelections();
});



