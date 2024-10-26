from django.shortcuts import render

# Create your views here.

#TUtorial aqui mero haces una funcion para que se renderize una nueva vista html que crees
#1. defines la funcion
#2 regresas el render que es una funcion que ya existe
#3 le dises la ruta donde esta, si esta ddentro de una carpeta dentro de templates le das el nombre, si solo esta en templates asi queda

#Esta es para el login v:
def index(request):
    return render(request, 'index.html')

#request de Alex
def compra_1(request):
    return render(request, 'compra_venta/compra.html')

def venta_1(request):
    return render(request, 'compra_venta/venta.html')

#request del perro de harry
def ajustes_1(request):
    return render(request, 'ajustes_caja/ajustes_1.html')

#request de francisco

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

#request de la huevona de Adri

def panel_control(request):
    return render(request, 'panel_control/panel.html')


def pantalla_carga(request):
    return render(request, 'p_carga.html')