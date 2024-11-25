from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction, Day_Report
from django.utils import timezone

# Create your views here.


#@login_required
def ajustes_1(request):

    today = timezone.now().date()
    money = Day_Report.objects.filter(Day=today)
    hora_actual = timezone.now()

    money_all=Day_Report.objects.all()
    
    # Consolidar el dinero final (opcional)
    final_money = sum(report.Final_Money for report in money) if money else 0

    box_money = {'final_money': final_money}
    
    return render(request, 'ajustes_1.html', {'box_money': box_money, 'money_all': money_all, 'hora_actual':hora_actual})