from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import Transaction, Day_Report
from django.utils.timezone import make_aware, now
from datetime import datetime, timezone
from django.core.paginator import Paginator

from django.utils.timezone import localtime, now
from datetime import time

@login_required
def ajustes_1(request):

    today_start = localtime(now()).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = localtime(now()).replace(hour=23, minute=59, second=59, microsecond=999999)


    in_ga = Transaction.objects.filter(
        Date__range=(today_start, today_end),
        Transaction_Type__in=["INVESTMENT", "EXPENSE"]
    )

   
    materials_p = Paginator(in_ga, 5)
    page_numb = request.GET.get('page')
    show_page = materials_p.get_page(page_numb)

    dinero_en_caja = sum(
        trans.Total if trans.Transaction_Type == "INVESTMENT" else -trans.Total
        for trans in in_ga
    )

    error_message = None

    if request.method == "POST":
        tipo_operacion = request.POST.get('tipo_operacion')
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')

        if tipo_operacion and monto and descripcion:
            try:
                monto = float(monto)
                if tipo_operacion == "EXPENSE" and monto > dinero_en_caja:
                    error_message = "El gasto excede el dinero disponible en caja."
                else:
                    nueva_trans = Transaction.objects.create(
                        User=request.user,
                        Total=monto,
                        Discount=0,
                        Transaction_Type=tipo_operacion,
                        Description=descripcion,
                        Status="COMPLETED",
                        Date=now()  
                    )
                    nueva_trans.save()
                    return redirect('ajustes_1')
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
                error_message = "Ocurrió un error al procesar la transacción."

    return render(request, 'ajustes_1.html', {
        'box_money': {'final_money': dinero_en_caja},
        'money_all': dinero_en_caja,
        'hora_actual': now(),
        'in_ga': in_ga,
        'dinero_en_caja': dinero_en_caja,
        'show_page': show_page,
        'error_message': error_message
    })
