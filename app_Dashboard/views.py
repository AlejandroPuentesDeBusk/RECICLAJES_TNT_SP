from django.utils.timezone import localtime, now
from django.shortcuts import render
from mainapp.models import Transaction_Details, Material
from django.core.paginator import Paginator
from django.utils import timezone

def dashboard(request):
    hora = timezone.now
    today = timezone.now
    today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = localtime(now()).replace(hour=23, minute=59, second=59, microsecond=999999)

    print(f"Rango: {today_start} - {today_end}")

    # Diccionario para traducir tipos de transacción
    transaction_type_mapping = {
        'SALE': 'Venta',
        'PURCHASE': 'Compra',
        'INVESTMENT': 'Inversión',
        'EXPENSE': 'Gasto'
    }

    # Filtrar detalles de transacciones del día actual
    transaction_details = Transaction_Details.objects.filter(
        Transaction__Date__range=(today_start, today_end),
        Transaction__Transaction_Type__in=['SALE', 'PURCHASE']
    ).select_related('Material', 'Transaction')  # Optimizamos consultas

    # Traducir tipos de transacción antes de pasarlos al contexto
    translated_transactions = []
    for detail in transaction_details:
        translated_transaction = detail
        transaction_type = detail.Transaction.Transaction_Type
        translated_transaction.Transaction.Transaction_Type = transaction_type_mapping.get(transaction_type, transaction_type)
        translated_transactions.append(translated_transaction)

    # Paginación de transacciones traducidas
    transaction_paginator = Paginator(translated_transactions, 5)
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
        'hora': hora,
    }
    return render(request, 'dash.html', context)