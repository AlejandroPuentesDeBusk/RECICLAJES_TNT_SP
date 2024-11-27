from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import Transaction, Day_Report
from django.utils.timezone import make_aware, now
from datetime import datetime, timezone  # Importa timezone de la biblioteca estándar

@login_required
def ajustes_1(request):
    # Fecha actual en UTC
    today = now().date()
    start_of_day = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)

    print(f"Rango calculado en UTC: {start_of_day} - {end_of_day}")  # Depuración

    # Filtrar transacciones del día (inversiones y gastos)
    in_ga = Transaction.objects.filter(
        Date__range=(start_of_day, end_of_day),
        Transaction_Type__in=["INVESTMENT", "EXPENSE"]
    )

    # Calcular el dinero en caja
    dinero_en_caja = 0
    for trans in in_ga:
        if trans.Transaction_Type == "INVESTMENT":
            dinero_en_caja += trans.Total  
        elif trans.Transaction_Type == "EXPENSE":
            dinero_en_caja -= trans.Total  

    print(f"Dinero en caja calculado: {dinero_en_caja}") 

 
    money = Day_Report.objects.filter(Day=today)
    final_money = sum(report.Final_Money for report in money) if money else 0

  
    box_money = {'final_money': final_money}


    if request.method == "POST":
        tipo_operacion = request.POST.get('tipo_operacion')
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')

        print(f"Formulario recibido: Tipo operación={tipo_operacion}, Monto={monto}, Descripción={descripcion}")

        if tipo_operacion and monto and descripcion:
            try:
                monto = float(monto)
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
                print(f"Transacción creada: {nueva_trans.id}")
                return redirect('ajustes_1')
            except Exception as e:
                print(f"Error al crear la transacción: {e}")

    return render(request, 'ajustes_1.html', {
        'box_money': box_money,
        'money_all': money,
        'hora_actual': now(),
        'in_ga': in_ga,
        'dinero_en_caja': dinero_en_caja  
    })