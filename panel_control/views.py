from django.shortcuts import render
from mainapp.models import Transaction,Transaction_Details
#agregando los modelos del material
from .models import Material
# Create your views here.

#esa es para importar la info de models de la base de datos 
#solo debe haber una

def panel_control(request):#para que agarre la bd agregue materiales
    materiales = Material.objects.all()
    return render(request, 'panel.html', {'materiales': materiales})

def personal(request):
    return render(request, 'personal.html')

def transacciones(request):
    return render(request, 'transacciones.html')

def materiales(requets):
    return render (requets, 'materiales.html')

def cortes(request):
    return render (request, 'cortes.html')
