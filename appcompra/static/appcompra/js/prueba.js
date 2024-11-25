document.addEventListener('DOMContentLoaded', function () {
    // Detect if the page was reloaded via the browser's reload button
    const navigationEntry = performance.getEntriesByType("navigation")[0];

    if (navigationEntry.type === 'reload') {
        // The page was reloaded via the reload button or location.reload()
        // Clear the localStorage
        localStorage.removeItem('selectedMaterials');
        localStorage.removeItem('tipoOperacionSeleccionado');
        localStorage.removeItem('tipoCargoSeleccionado');
    }

    const checkboxes = document.querySelectorAll('.cajita');
    const lista_Material = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo');
    const tipoOperacionSelect = document.getElementById('tipo_operacion');
    const total_final = document.getElementById('total_general');
    const discount_int = document.getElementById('discount');
    const extra_charge_int = document.getElementById('extra_charge');
    const realizar_compra_btn = document.getElementById('realizar_compra');

    const selectedMaterialsKey = 'selectedMaterials';
    let savedSelections = JSON.parse(localStorage.getItem(selectedMaterialsKey)) || [];

    // Restore selections on page load
    let savedTipoOperacion = localStorage.getItem('tipoOperacionSeleccionado');
    let savedTipoCargo = localStorage.getItem('tipoCargoSeleccionado');

    if (savedTipoOperacion) {
        tipoOperacionSelect.value = savedTipoOperacion;
    }

    if (savedTipoCargo) {
        tipoCargoSelect.value = savedTipoCargo;
    }

    function areSelectionsValid() {
        return tipoOperacionSelect.value !== "" && tipoCargoSelect.value !== "";
    }

    function showSelectionError() {
        alert("Por favor, selecciona el tipo de operación y el tipo de cargo antes de agregar materiales.");
    }

    tipoOperacionSelect.addEventListener('change', function () {
        localStorage.setItem('tipoOperacionSeleccionado', tipoOperacionSelect.value);
    });

    tipoCargoSelect.addEventListener('change', function () {
        localStorage.setItem('tipoCargoSeleccionado', tipoCargoSelect.value);
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (!areSelectionsValid()) {
                showSelectionError();
                checkbox.checked = false;
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
                // Remove material from savedSelections
                const index = savedSelections.findIndex(item => item.materialId === materialId);
                if (index > -1) {
                    savedSelections.splice(index, 1);
                    localStorage.setItem(selectedMaterialsKey, JSON.stringify(savedSelections));
                }
            }

            actualizar_total();
            checkCartAndToggleSelects(); // Update the select elements based on cart contents
        });
    });

    function obtenerPrecio(checkbox) {
        const operacion = tipoOperacionSelect.value;
        const tipoCargo = tipoCargoSelect.value;
        return operacion === 'compra'
            ? parseFloat(checkbox.getAttribute(`data-${tipoCargo}`))
            : parseFloat(checkbox.getAttribute(`data-${tipoCargo.replace('Purchase', 'Sale')}`));
    }

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
        checkCartAndToggleSelects(); // Update the select elements based on cart contents
    }

    function guardarSeleccion(materialData) {
        const index = savedSelections.findIndex(item => item.materialId === materialData.materialId);

        if (index > -1) {
            savedSelections[index] = materialData;
        } else {
            savedSelections.push(materialData);
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
            <input type="number" class="cant_total" min="0" placeholder="Cantidad" value="${cantidad}" data-price="${price}">
            <span class="precio_total">${(cantidad * price).toFixed(2)}</span> MXN
        `;

        const inputCantidad = listItem.querySelector('.cant_total');
        inputCantidad.addEventListener('input', function () {
            const nuevaCantidad = parseFloat(this.value) || 0;
            listItem.querySelector('.precio_total').textContent = (nuevaCantidad * price).toFixed(2);

            const updatedMaterialData = { materialId, materialName, price, image, cantidad: nuevaCantidad };
            guardarSeleccion(updatedMaterialData);

            actualizar_total();
        });
    }

    // Add event listeners to discount and extra charge inputs to update total when they change
    discount_int.addEventListener('input', actualizar_total);
    extra_charge_int.addEventListener('input', actualizar_total);

    function actualizar_total() {
        let total_general = 0;
        lista_Material.querySelectorAll('li').forEach(listItem => {
            const cantidadInput = listItem.querySelector('.cant_total');
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const price = parseFloat(cantidadInput.getAttribute('data-price')) || 0;
            total_general += cantidad * price;
        });

        // Calculate the maximum allowed discount (5% of total_general)
        const max_discount = total_general * 0.05;

        // Update the 'max' attribute of the discount input field
        discount_int.max = max_discount.toFixed(2);

        // Get the discount value entered by the user
        let discount = parseFloat(discount_int.value) || 0;

        // Validate and adjust the discount
        if (discount > max_discount) {
            discount = max_discount;
            discount_int.value = discount.toFixed(2);
            // Optionally, display a message to the user
            alert('El descuento no puede ser mayor al 5% del total. Se ha ajustado al máximo permitido.');
        }

        const extra_charge = parseFloat(extra_charge_int.value) || 0;
        const total_con_descuento = total_general - discount + extra_charge;
        total_final.textContent = `${total_con_descuento.toFixed(2)} MXN`;

        realizar_compra_btn.disabled = total_con_descuento <= 0;
    }

    // Function to check if cart is empty and toggle the select elements
    function checkCartAndToggleSelects() {
        const hasMaterialsInCart = savedSelections.length > 0;

        // If there are materials in the cart, disable the select elements
        if (hasMaterialsInCart) {
            tipoOperacionSelect.disabled = true;
            tipoCargoSelect.disabled = true;
        } else {
            tipoOperacionSelect.disabled = false;
            tipoCargoSelect.disabled = false;
        }
    }

    // Initial check on page load
    checkCartAndToggleSelects();

    restoreSelections();
});







