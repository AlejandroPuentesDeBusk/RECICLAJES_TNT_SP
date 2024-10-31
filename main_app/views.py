from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

Users = get_user_model()


def is_owner(users):
    return users.is_active and users.is_superuser

def is_employee(users):
    return users.is_active 

#el index es ella ventana del login
def index(request):
    return render(request, 'index.html')


#request de Alex

def compra_1(request):
    return render(request, 'compra_venta/compra.html')

@login_required
def venta_1(request):
    return render(request, 'compra_venta/venta.html')

@login_required
def ajustes_1(request):
    return render(request, 'ajustes_caja/ajustes_1.html')

#request de francisco
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

#request de Adri
@login_required
@user_passes_test(is_owner) 
def panel_control(request):
    return render(request, 'panel_control/panel.html')

@login_required
def pantalla_carga(request):
    return render(request, 'p_carga.html')