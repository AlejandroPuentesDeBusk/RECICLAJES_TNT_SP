from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction, Day_Report
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404

Users = get_user_model()





def cv(request):
    materials = Material.objects.all()
    money= Day_Report.objects.latest('Day')
    final_money= money.Final_Money

    box_money = {'final_money': final_money}

    #paginador
    materials_p = Paginator(materials, 8)
    page_numb = request.GET.get('page')
    show_page = materials_p.get_page(page_numb)




    return render(request, 'compra_venta/com_ven.html', {'show_page': show_page, 'box_money':box_money})