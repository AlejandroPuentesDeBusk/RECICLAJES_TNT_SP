from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction, Day_Report
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.


#@login_required
def ajustes_1(request):

    today = timezone.now().date()
    #para que solo sean de hoy
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    hora_actual = timezone.now()


    in_ga = Transaction.objects.filter(
        Date__range=(start_of_day, end_of_day),
        Transaction_Type__in=["INVESTMENT", "EXPENSE"]
    )


    money = Day_Report.objects.filter(Day=today)


    #Dinero del dia de hoy
    money_all=Day_Report.objects.all()
    
    # Consolidar el dinero final (opcional)
    final_money = sum(report.Final_Money for report in money) if money else 0

    box_money = {'final_money': final_money}
    
    return render(request, 'ajustes_1.html', {'box_money': box_money, 'money_all': money_all, 'hora_actual':hora_actual, 'in_ga':in_ga})