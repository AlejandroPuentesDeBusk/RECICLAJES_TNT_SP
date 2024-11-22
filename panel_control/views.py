from django.shortcuts import render
from mainapp import views
from django.contrib.auth import get_user_model
from mainapp.models import Material


Users = get_user_model()

# Create your views here.
#esa es para importar la info de models de la base de datos 

def panel_control(request):
    materials = Material.objects.all()
    return render(request, 'panel.html',{'materials': materials})

def personal(request):
    return render(request, 'personal.html', {
        'title': 'Panel de Control | Personal',
        'section': 'Panel de Control',
        'subsection': 'Ajustes de Personal'
    })

def transacciones(request):
    return render(request, 'transacciones.html', {
        'title': 'Panel de Control | Transacciones',
        'section': 'Panel de Control',
        'subsection': 'Ajustes de Transacciones',
    })

def materiales(request):
    materials = Material.objects.all()
    return render (request, 'materiales.html', {
        'title': 'Panel de Control | Materiales',
        'section': 'Panel de Control',
        'subsection': 'Ajustes de Materiales',
        'materials': materials
    })

def cortes(request):
    return render (request, 'cortes.html', {
        'title': 'Panel de Control | Cortes',
        'section': 'Panel de Control',
        'subsection': 'Historial de Cortes'
    })
