from django.shortcuts import render
from datetime import date
from mainapp.models import Transaction, Transaction_Details, Material
from django.db import models
from django.core.paginator import Paginator

def dashboard(request):
    # OBTENER TRANSACCIONES
    transacciones = Transaction_Details.objects.select_related('Material', 'Transaction').order_by('-Transaction__Date')[:100].values(
        'Transaction__Transaction_Type',
        'Material__Material_Type',
        'Quantity',
        'Price',
        'Transaction__Description',
        'Transaction__Date',
        'Transaction__Status'
    )

    # TRADUCCIÓN DE VALORES
    TRANSLATION_TYPES = {
        'SALE': 'Venta',
        'PURCHASE': 'Compra',
        'COMPLETED': 'Completada',
        'PENDING': 'Pendiente',
        'CANCELED': 'Cancelada'
    }
    for transaccion in transacciones:
        transaccion['Transaction__Transaction_Type'] = TRANSLATION_TYPES.get(transaccion['Transaction__Transaction_Type'], transaccion['Transaction__Transaction_Type'])
        transaccion['Transaction__Status'] = TRANSLATION_TYPES.get(transaccion['Transaction__Status'], transaccion['Transaction__Status'])

    # PAGINACIÓN
    materials_p = Paginator(transacciones, 10)  # Muestra 10 registros por página
    page_numb = request.GET.get('page')  # Obtiene el número de página actual
    show_page = materials_p.get_page(page_numb)  # Obtiene los registros de la página actual

    # MATERIAL MÁS COMPRADO Y VENDIDO DEL DÍA
    hoy = date.today()
    transacciones_hoy = Transaction.objects.filter(Transaction_Type='PURCHASE', Date__date=hoy)
    detalles_hoy = Transaction_Details.objects.filter(Transaction__in=transacciones_hoy).values('Material__Material_Type').annotate(total=models.Sum('Quantity')).order_by('-total')
    material_mas_comprado = detalles_hoy.first()

    transacciones_hoy_venta = Transaction.objects.filter(Transaction_Type='SALE', Date__date=hoy)
    detalles_hoy_venta = Transaction_Details.objects.filter(Transaction__in=transacciones_hoy_venta).values('Material__Material_Type').annotate(total=models.Sum('Quantity')).order_by('-total')
    material_mas_vendido = detalles_hoy_venta.first()

    # PRODUCTO CON MÁS STOCK
    producto_mas_stock = Material.objects.annotate(stock=models.F('transactions__transaction_details__Quantity')).order_by('-stock').first()

    # CONTEXTO PARA LA PLANTILLA
    context = {
        'show_page': show_page,  # Cambiar a la página paginada
        'material_mas_comprado': material_mas_comprado,
        'material_mas_vendido': material_mas_vendido,
        'producto_mas_stock': producto_mas_stock,
    }

    return render(request, 'dash.html', context)
