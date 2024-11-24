document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.cajita');
    const lista_Material = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo');
    const tipoOperacionSelect = document.getElementById('tipo_operacion');
    const total_final = document.getElementById('total_general');
    const discount_int = document.getElementById('discount');
    const extra_charge_int = document.getElementById('extra_charge');
    const realizar_compra_btn = document.getElementById('realizar_compra');

    const selectedMaterialsKey = 'selectedMaterials'; // Clave global para almacenar la selección en localStorage

    // Cargar las selecciones guardadas de localStorage
    let savedSelections = JSON.parse(localStorage.getItem(selectedMaterialsKey)) || [];

    // Restaurar selección desde localStorage
    function restoreSelections() {
        console.log('Restaurando selecciones:', savedSelections);

        // Limpiar la lista actual de materiales seleccionados en la calculadora
        lista_Material.innerHTML = '';

        // Iterar sobre las selecciones guardadas
        savedSelections.forEach(savedItem => {
            const materialId = savedItem.materialId;
            const checkbox = document.querySelector(`.cajita[data-material="${materialId}"]`);
            if (checkbox) {
                checkbox.checked = true;
            } else {
                // Si el checkbox no está en la página actual, no podemos marcarlo
                console.log(`El material ID ${materialId} no está en esta página`);
            }
            // Agregar o actualizar el material en la calculadora
            actualizarMaterialEnCalculadora(savedItem);
        });

        actualizar_total();
    }

    // Guardar el estado actual en localStorage
    function guardarSeleccion(materialData) {
        const index = savedSelections.findIndex(item => item.materialId === materialData.materialId);

        if (materialData.cantidad > 0) {
            if (index > -1) {
                savedSelections[index] = materialData; // Actualizar si ya existe
            } else {
                savedSelections.push(materialData); // Agregar nuevo material
            }
        } else if (index > -1) {
            savedSelections.splice(index, 1); // Eliminar si la cantidad es 0
        }

        localStorage.setItem(selectedMaterialsKey, JSON.stringify(savedSelections)); // Guardar en localStorage
    }

    // Obtener el precio según operación y tipo de cargo
    function obtenerPrecio(checkbox) {
        const operacion = tipoOperacionSelect.value; // "compra" o "venta"
        const tipoCargo = tipoCargoSelect.value; // "Wholesale_Purchase_Price" o "Retail_Purchase_Price"
        return operacion === 'compra'
            ? parseFloat(checkbox.getAttribute(`data-${tipoCargo}`))
            : parseFloat(checkbox.getAttribute(`data-${tipoCargo.replace('Purchase', 'Sale')}`));
    }

    // Actualizar el total
    function actualizar_total() {
        let total_general = 0;
        lista_Material.querySelectorAll('.precio_total').forEach(span => {
            total_general += parseFloat(span.textContent) || 0;
        });

        const discount = parseFloat(discount_int.value) || 0;
        const extra_charge = parseFloat(extra_charge_int.value) || 0;
        const total_con_descuento = total_general - discount + extra_charge;
        total_final.textContent = `${total_con_descuento.toFixed(2)} MXN`;

        // Habilitar o deshabilitar el botón de compra
        realizar_compra_btn.disabled = total_con_descuento <= 0;
    }

    // Agregar o actualizar un material en la calculadora
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
            guardarSeleccion(updatedMaterialData); // Guardar la cantidad actualizada

            if (nuevaCantidad <= 0) {
                // Si la cantidad es 0 o menos, eliminar de la calculadora y desmarcar el checkbox
                lista_Material.removeChild(listItem);
                const checkbox = document.querySelector(`.cajita[data-material="${materialId}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
            }

            actualizar_total();
        });
    }

    // Manejar eventos de selección de los checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const materialId = checkbox.getAttribute('data-material');
            const materialName = checkbox.getAttribute('data-material-name');
            const price = obtenerPrecio(checkbox);
            const image = checkbox.getAttribute('data-image');

            if (checkbox.checked) {
                const materialData = { materialId, materialName, price, image, cantidad: 0 };
                guardarSeleccion(materialData);
                actualizarMaterialEnCalculadora(materialData);
            } else {
                // Eliminar material de la calculadora y de las selecciones
                const listItem = lista_Material.querySelector(`li[data-material="${materialId}"]`);
                if (listItem) {
                    lista_Material.removeChild(listItem);
                }
                guardarSeleccion({ materialId, cantidad: 0 });
            }

            actualizar_total();
        });
    });

    // Restaurar selección al cargar la página
    restoreSelections();

    // Actualizar precios al cambiar el tipo de operación o tipo de cargo
    function actualizarPrecios() {
        savedSelections.forEach(item => {
            const checkbox = document.querySelector(`.cajita[data-material="${item.materialId}"]`);
            const price = obtenerPrecio(checkbox || { getAttribute: () => item.price });
            item.price = price;
            actualizarMaterialEnCalculadora(item);
            guardarSeleccion(item);
        });
        actualizar_total();
    }

    tipoCargoSelect.addEventListener('change', actualizarPrecios);
    tipoOperacionSelect.addEventListener('change', actualizarPrecios);

    // Eventos para actualizar el total con descuento y cargos extras
    discount_int.addEventListener('input', actualizar_total);
    extra_charge_int.addEventListener('input', actualizar_total);
});



