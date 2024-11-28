from django.utils.timezone import localtime, now
from django.shortcuts import render
from mainapp.models import Transaction_Details, Material
from django.core.paginator import Paginator

def dashboard(request):
    today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = localtime(now()).replace(hour=23, minute=59, second=59, microsecond=999999)

    # Filtrar detalles de transacciones del día actual
    transaction_details = Transaction_Details.objects.filter(
        Transaction__Date__range=(today_start, today_end),
        Transaction__Transaction_Type__in=['COMPRA', 'VENTA']
    ).select_related('Material', 'Transaction')  # Optimizamos consultas

    # Paginación
    paginator = Paginator(transaction_details, 5)
    page_number = request.GET.get('page')
    show_page = paginator.get_page(page_number)

    # Obtener todos los materiales
    materials = Material.objects.all()

    context = {
        'show_page': show_page,
        'today': today_start.date(),
        'materials': materials,
    }
    return render(request, 'dash.html', context)

