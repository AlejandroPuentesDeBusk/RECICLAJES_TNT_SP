from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction
from django.utils import timezone

Users = get_user_model()

#__________________________________CRUD MENU CV_____________________________________________________

def menu_cv(request):
    today_t = Transaction.objects.filter(Date__date=timezone.now().date())
    return render(request, 'compra_venta/menu_cv.html', {'today_t': today_t})

#_________________________________CRUD Y REQUEST COMPRAS____________________________________________

def compra_1(request):
    materials = Material.objects.all()
    return render(request, 'compra_venta/compra.html', {'materials': materials})

def insert_purachase(request):
    if request.method == "POST":
        total = request.POST.get("total")

#_________________________________CRUD Y REQUEST VENTAS___________________________________________

def venta_1(request):
    return render(request, 'compra_venta/venta.html')



def cv(request):
    materials = Material.objects.all()
    return render(request, 'compra_venta/cv.html', {'materials': materials})
