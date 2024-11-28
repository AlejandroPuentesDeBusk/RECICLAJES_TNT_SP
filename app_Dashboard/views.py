from django.utils.timezone import localtime, now
from django.shortcuts import render
from mainapp.models import Transaction_Details, Material
from django.core.paginator import Paginator

def dashboard(request):
    today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = localtime(now()).replace(hour=23, minute=59, second=59, microsecond=999999)

    print(f"Rango: {today_start} - {today_end}")


    # Filtrar detalles de transacciones del día actual
    transaction_details = Transaction_Details.objects.filter(
        Transaction__Date__range=(today_start, today_end),
        Transaction__Transaction_Type__in=['PURACHASE', 'SELL']
    ).select_related('Material', 'Transaction')  # Optimizamos consultas

    # Paginación de transacciones
    transaction_paginator = Paginator(transaction_details, 5)
    transaction_page_number = request.GET.get('transaction_page')
    show_page = transaction_paginator.get_page(transaction_page_number)

    # Obtener todos los materiales con paginación
    materials = Material.objects.all()
    material_paginator = Paginator(materials, 4)
    material_page_number = request.GET.get('material_page')
    materials_page = material_paginator.get_page(material_page_number)

    context = {
        'show_page': show_page,
        'materials_page': materials_page,
        'today': today_start.date(),
    }
    return render(request, 'dash.html', context)


