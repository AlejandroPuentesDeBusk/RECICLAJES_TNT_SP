document.addEventListener('DOMContentLoaded', () => {
    const filterBtn = document.getElementById('filter-btn');
    const tableRows = document.querySelectorAll('#materials-table tr');
    const purchaseHeader = document.getElementById('price-purchase-header');
    const saleHeader = document.getElementById('price-sale-header');
    filterBtn.addEventListener('change', () => {
        const filterValue = filterBtn.value; 
        tableRows.forEach(row => {
            if (!filterValue || row.dataset.operation === filterValue) {
                row.style.display = ''; 
            } else {
                row.style.display = 'none'; 
            }
        });
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
    });
});
