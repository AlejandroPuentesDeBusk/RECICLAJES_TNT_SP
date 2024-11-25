from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction, Day_Report
from django.utils import timezone

# Create your views here.


#@login_required
def ajustes_1(request):
    money= Day_Report.objects.latest('Day')
    final_money= money.Final_Money

    box_money = {'final_money': final_money}


    return render(request, 'ajustes_1.html',{'box_money': box_money})

    money= Day_Report.objects.latest('Day')
    final_money= money.Final_Money


    box_money = {'final_money': final_money}


    return render(request, 'ajustes_1.html',{'box_money': box_money})