from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from.models import Material, Transaction
from django.utils import timezone

Users = get_user_model()


def is_owner(users):
    return users.is_active and users.is_superuser

def is_employee(users):
    return users.is_active 

#el index es ella ventana del login
def index(request):
    return render(request, 'index.html')

#@login_required
def pantalla_carga(request):
    return render(request, 'p_carga.html')

def error404(request,exception):
    return render(request, 'mainapp/404.html')




#___________YA LO MOVI A APPCOMPRA___________________CRUD MENU CV_____________________________________________________

#def menu_cv(request):
 #   today_t = Transaction.objects.filter(Date__date= timezone.now().date())
  #  return render(request, 'compra_venta/menu_cv.html',{'today_t':today_t})

#____________YA LO MOVI A APPCOMPRA________________CRUD Y REQUEST COMPRAS____________________________________________


#def compra_1(request):
 #   materials = Material.objects.all()
  #  return render(request, 'compra_venta/compra.html', {'materials':materials})

#def insert_purachase(request):
 #   if request.method == "POST":
  #      total = request.POST.get("total")


#_____________YA LO MOVI A APP COMPRA______________CRUD Y REQUEST VENTAS___________________________________________


#@login_required
#def venta_1(request):
 #   return render(request, 'compra_venta/venta.html')



#________________________________________________________________________________________________


#__________________SE MOVIO A CAJA____________###
#@login_required
#def ajustes_1(request):
    #return render(request, 'ajustes_caja/ajustes_1.html')


#__________________SE MOVIO A DAHSBOARD____________###
#request de francisco
#@login_required
#def dashboard(request):
    #return render(request, 'dashboard/dashboard.html')

#request de Adri muy floja por cierto
#@login_required
#@user_passes_test(is_owner) 
#def panel_control(request):
#    return render(request, 'panel_control/panel.html')

#_____________________MOVIMOS ESTOS_____________________

#def panel_control_personal(request):
#    return render(request, 'panel_control/personal.html')

#def panel_control_transacciones(request):
#    return render(request, 'panel_control/transacciones.html')



#-----------views aqui hacer la query de insert-------------
