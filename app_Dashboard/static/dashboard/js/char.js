document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('myChart').getContext('2d');

    const materialName = "{{ material_mas_vendido.Material_Type|default:'' }}";
    const materialQuantity = "{{ material_mas_vendido.total|default:0 }}";

    const data = {
        labels: [materialName],
        datasets: [{
            label: 'Cantidad Vendida (kg)',
            data: [materialQuantity],
            backgroundColor: ['rgba(75, 192, 192, 0.2)'],
            borderColor: ['rgba(75, 192, 192, 1)'],
            borderWidth: 1,
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
