from django.shortcuts import render, redirect
from mainapp import views
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction, Day_Report
from django.core.paginator import Paginator
from django.db.models import Q

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
    search_query = request.GET.get('search', '').lower()  # Obtener lo que se ingreso en el elemento con el name "search", en minuscula para hacer el mapeo
    # transactions = Transaction.objects.all()

    transaction_type_mapping = {
        'venta': 'SALE',
        'compra': 'PURCHASE',
        'inversión': 'INVESTMENT',
        'gasto': 'EXPENSE'
    }

    # verifica las coincidencias de la busqueda y el mapeo
    transaction_type = transaction_type_mapping.get(search_query)

    #  para poner diferentes condiciones de filtro con Q
    if transaction_type:
        transactions = Transaction.objects.filter(
            Q(Transaction_Type=transaction_type)
        )
    else:
        # En caso de que no se encuentre un mapeo, buscar en otros campos
        transactions = Transaction.objects.filter(
            Q(Description__icontains=search_query) | 
            Q(Total__icontains=search_query)  
        )

    if not search_query:
        transactions = Transaction.objects.all()
    
    return render(request, 'transacciones.html', {
        'title': 'Panel de Control | Transacciones',
        'section': 'Panel de Control',
        'subsection': 'Ajustes de Transacciones',
        'transactions': transactions,
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
    search_query = request.GET.get('search', '')  # Obtener lo que se busca
    
    if search_query:
        reports = Day_Report.objects.filter(
            Day__icontains=search_query  # O cualquier otro filtro relevante
        )
    else:
        reports = Day_Report.objects.all()
    reports = Day_Report.objects.all()
    return render (request, 'cortes.html', {
        'title': 'Panel de Control | Cortes',
        'section': 'Panel de Control',
        'subsection': 'Historial de Cortes',
        'reports': reports,
        'search_query': search_query,
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