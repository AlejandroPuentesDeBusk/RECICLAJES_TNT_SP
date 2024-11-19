from django.shortcuts import render
from mainapp.models import Transaction,Transaction_Details
# Create your views here.
#esa es para importar la info de models de la base de datos 
#solo debe haber una
def panel_control(request):
    return render(request, 'panel.html')

def personal(request):
    return render(request, 'personal.html')

def transacciones(request):
    return render(request, 'transacciones.html')

def materiales(request):
    return render (request, 'materiales.html')

def cortes(request):
    return render (request, 'cortes.html')
