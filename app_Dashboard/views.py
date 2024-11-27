from django.utils.timezone import localtime, now
from django.shortcuts import render
from mainapp.models import Transaction
from django.core.paginator import Paginator

def dashboard(request):


    #asi emparejamos las fechas, que luego se desfasa, time zone es la buena, la otra da mal tiempo

    today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = localtime(now()).replace(hour=23, minute=59, second=59, microsecond=999999)

    transactions = Transaction.objects.filter(
        Date__range=(today_start, today_end),
        Transaction_Type__in=['COMPRA', 'VENTA']  
    )

    #esto pal paginado
    materials_p = Paginator(transactions, 10)
    page_numb = request.GET.get('page')
    show_page = materials_p.get_page(page_numb)


    context = {
        'today': today_start.date(),
        'show_page':show_page
    }
    return render(request, 'dash.html', context)
