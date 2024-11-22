from django.shortcuts import render, redirect
from mainapp import views
from django.contrib.auth import get_user_model
from mainapp.models import Material
from django.core.paginator import Paginator

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

def error404(request,exception):
    return render(request, 'mainapp/404.html')

def is_owner(users):
    return users.is_active and users.is_superuser

def is_employee(users):
    return users.is_active 

def materiales(request):
    material_list = Material.objects.all()  # Obtener todos los materiales de la mendiga tabla
    paginator = Paginator(material_list, 5)  # 5 materiales por página es horrible tener muchas
    page_number = request.GET.get('page')  # Obtener el número de página desde la URL es un dolor de huevos
    page_obj = paginator.get_page(page_number)  # Obtener la página solicitada que jode
    search_query = request.GET.get('search','')
    # Filtrar los materiales según el término de búsqueda
    if search_query:
        materials_list = Material.objects.filter(Material_Type__icontains=search_query)
    else:
        materials_list = Material.objects.all()
    
    # Configurar la paginación
    paginator = Paginator(materials_list, 5)  # 5 materiales por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'materiales.html', {
        'page_obj': page_obj,
        'search_query': search_query
        })