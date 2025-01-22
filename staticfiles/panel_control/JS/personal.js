document.addEventListener('DOMContentLoaded', () => {
    const filterBtn = document.getElementById('filter-btn');
    const tableRows = document.querySelectorAll('#materials-table tr');
    const purchaseHeader = document.getElementById('price-purchase-header');
    const saleHeader = document.getElementById('price-sale-header');

    // Recuperar selección guardada en localStorage o usar el valor por defecto 'venta'
    const savedFilter = localStorage.getItem('selectedFilter') || 'venta';
    filterBtn.value = savedFilter;

    // Función para aplicar filtro
    const applyFilter = (filterValue) => {
        tableRows.forEach(row => {
            if (!filterValue || row.dataset.operation === filterValue) {
                row.style.display = ''; // Mostrar fila
            } else {
                row.style.display = 'none'; // Ocultar fila
            }
        });

        // Cambiar encabezados según el filtro
        if (filterValue === 'compra') {
            purchaseHeader.textContent = 'Precio Compra Mayorista';
            saleHeader.textContent = 'Precio Venta Mayorista';
        } else if (filterValue === 'venta') {
            purchaseHeader.textContent = 'Precio Compra Minorista';
            saleHeader.textContent = 'Precio Venta Minorista';
        } else {
            purchaseHeader.textContent = 'Precio Compra';
            saleHeader.textContent = 'Precio Venta';
        }
    };

    // Aplicar filtro al cargar la página
    applyFilter(savedFilter);

    // Actualizar filtro al cambiar la selección
    filterBtn.addEventListener('change', () => {
        const filterValue = filterBtn.value;

        // Guardar la selección en localStorage
        localStorage.setItem('selectedFilter', filterValue);

        // Aplicar filtro
        applyFilter(filterValue);
    });
});


//al final django no me saca la ruta usare el atributo script