from django.shortcuts import render
from mainapp.models import Transaction,Transaction_Details
# Create your views here.
#esa es para importar la info de models de la base de datos 
#solo debe haber una
def panel_control(request):
    return render(request, 'panel.html')

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
    return render (request, 'materiales.html', {
        'title': 'Panel de Control | Materiales',
        'section': 'Panel de Control',
        'subsection': 'Ajustes de Materiales'
    })

def cortes(request):
    return render (request, 'cortes.html', {
        'title': 'Panel de Control | Cortes',
        'section': 'Panel de Control',
        'subsection': 'Historial de Cortes'
    })
