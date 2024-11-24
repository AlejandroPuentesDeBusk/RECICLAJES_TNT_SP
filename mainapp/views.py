from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from.models import Material, Transaction
from django.utils import timezone

from .forms import loginn
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

#Para el update de las tablas
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Material

Users = get_user_model()


def is_owner(users):
    return users.is_active and users.is_superuser

def is_employee(users):
    return users.is_active 

#el index es ella ventana del login
def index(request):
    return render(request, 'index.html')

@login_required
def pantalla_carga(request):
    return render(request, 'p_carga.html')

def error404(request,exception):
    return render(request, 'mainapp/404.html')

def login_view(request):
    if request.method == 'POST':
        form = loginn(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pantalla_carga')
            else:
                messages.error(request, "Credenciales no válidas")
        else:
            messages.error(request, "Formulario no válido")
    else:
        form=loginn()
    return render(request, 'Loginn.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada")
    return redirect('login')
#___________YA LO MOVI A APPCOMPRA___________________CRUD MENU CV_____________________________________________________

class UpdateMaterial(UpdateView):
    model = Material
    fields = ['Material_Type', 'Wholesale_Purchase_Price', 'Wholesale_Sale_Price', 'Retail_Purchase_Price', 'Retail_Sale_Price', 'image' ]
    template_name = 'update_material.html'
    success_url = reverse_lazy('materiales')


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
