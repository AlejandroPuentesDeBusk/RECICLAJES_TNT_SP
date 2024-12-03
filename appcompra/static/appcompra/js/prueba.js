document.addEventListener('DOMContentLoaded', function () {
    // Detectar si la página fue recargada
    const navigationEntry = performance.getEntriesByType("navigation")[0];

    if (navigationEntry.type === 'reload') {
        // La página fue recargada, limpiar el localStorage
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

    // Restaurar selecciones al cargar la página
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
                // Eliminar material de savedSelections
                const index = savedSelections.findIndex(item => item.materialId === materialId);
                if (index > -1) {
                    savedSelections.splice(index, 1);
                    localStorage.setItem(selectedMaterialsKey, JSON.stringify(savedSelections));
                }
            }

            actualizar_total();
            checkCartAndToggleSelects(); // Actualizar los selectores basados en el carrito
        });
    });

    function obtenerPrecio(checkbox) {
        const operacion = tipoOperacionSelect.value;
        const tipoCargo = tipoCargoSelect.value;

        let priceAttr = '';

        if (operacion === 'PURCHASE') {
            priceAttr = tipoCargo.toLowerCase();
        } else if (operacion === 'SALE') {
            // Reemplazar 'Purchase' por 'Sale' en el tipo de cargo
            priceAttr = tipoCargo.replace('Purchase', 'Sale').toLowerCase();
        }

        return parseFloat(checkbox.getAttribute(`data-${priceAttr}`)) || 0;
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
        checkCartAndToggleSelects(); // Actualizar los selectores basados en el carrito
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

    // Agregar eventos a los campos de descuento y cargo extra para actualizar el total
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

        // Calcular el descuento máximo permitido (5% del total general)
        const max_discount = total_general * 0.05;

        // Actualizar el atributo 'max' del campo de descuento
        discount_int.max = max_discount.toFixed(2);

        // Obtener el valor del descuento ingresado por el usuario
        let discount = parseFloat(discount_int.value) || 0;

        // Validar y ajustar el descuento
        if (discount > max_discount) {
            discount = max_discount;
            discount_int.value = discount.toFixed(2);
            alert('El descuento no puede ser mayor al 5% del total. Se ha ajustado al máximo permitido.');
        }

        const extra_charge = parseFloat(extra_charge_int.value) || 0;
        const total_con_descuento = total_general - discount + extra_charge;
        total_final.textContent = `${total_con_descuento.toFixed(2)} MXN`;

        realizar_compra_btn.disabled = total_con_descuento <= 0;
    }

    // Función para verificar si el carrito está vacío y deshabilitar los selectores
    function checkCartAndToggleSelects() {
        const hasMaterialsInCart = savedSelections.length > 0;

        if (hasMaterialsInCart) {
            tipoOperacionSelect.disabled = true;
            tipoCargoSelect.disabled = true;
        } else {
            tipoOperacionSelect.disabled = false;
            tipoCargoSelect.disabled = false;
        }
    }

    // Verificación inicial al cargar la página
    checkCartAndToggleSelects();

    restoreSelections();

    // Evento para el botón "Realizar Compra"
    realizar_compra_btn.addEventListener('click', function () {
        // Recolectar datos necesarios
        const materials = savedSelections.map(item => ({
            materialId: item.materialId,
            quantity: parseFloat(item.cantidad) || 0,
            price: parseFloat(item.price) || 0
        }));

        const data = {
            materials: materials,
            tipoOperacion: tipoOperacionSelect.value,
            tipoCargo: tipoCargoSelect.value,
            discount: parseFloat(discount_int.value) || 0,
            extra_charge: parseFloat(extra_charge_int.value) || 0,
            total: parseFloat(total_final.textContent) || 0,
            description: document.querySelector('#final_texto textarea').value
        };

        // Validar que las cantidades sean mayores a cero
        for (let material of materials) {
            if (material.quantity <= 0) {
                alert('La cantidad de cada material debe ser mayor a cero.');
                return;
            }
        }

        // Mostrar confirmación al usuario
        const confirmacion = confirm('¿Estás seguro de que deseas realizar esta operación?');

        if (!confirmacion) {
            // El usuario canceló la operación
            return;
        }

        // Enviar datos al servidor
        fetch(realizarCompraUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor.');
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                alert('Operación realizada con éxito.');
                // Limpiar selecciones y recargar la página
                localStorage.removeItem('selectedMaterials');
                localStorage.removeItem('tipoOperacionSeleccionado');
                localStorage.removeItem('tipoCargoSeleccionado');
                window.location.reload();
            } else {
                alert('Error al realizar la operación: ' + result.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al procesar la solicitud: ' + error.message);
        });
    });

    // Ya no es necesario obtener el token CSRF desde las cookies, ya que lo estamos pasando desde el HTML
});







