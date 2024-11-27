from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import Transaction, Day_Report
from django.utils.timezone import make_aware, now
from datetime import datetime, timezone

@login_required
def ajustes_1(request):
    # Fecha actual en UTC
    today = now().date()
    start_of_day = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)

    # Filtrar transacciones del día (inversiones y gastos)
    in_ga = Transaction.objects.filter(
        Date__range=(start_of_day, end_of_day),
        Transaction_Type__in=["INVESTMENT", "EXPENSE"]
    )

    # Calcular el dinero en caja
    dinero_en_caja = 0
    for trans in in_ga:
        if trans.Transaction_Type == "INVESTMENT":
            dinero_en_caja += trans.Total  # Sumar inversiones
        elif trans.Transaction_Type == "EXPENSE":
            dinero_en_caja -= trans.Total  # Restar gastos

    error_message = None

    # Procesar formulario si el método es POST
    if request.method == "POST":
        tipo_operacion = request.POST.get('tipo_operacion')
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')

        if tipo_operacion and monto and descripcion:
            try:
                monto = float(monto)

                # Validar si el gasto excede el dinero en caja
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
                        Date=now()  # Fecha actual en UTC
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
        'error_message': error_message  # Enviar mensaje de error a la plantilla
    })

