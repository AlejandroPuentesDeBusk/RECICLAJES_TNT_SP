///////////////FAVOR DE LEER NOVEDADES PARA QUE SEPAN QUE HACER////////////////
----------------Leean porfavor--------------------

Que hay de novedades aqui bueno se hicieron las siguientes actualizaciones
______________________Que Hacemos_________________________
Somos un grupo de estudiantes de Ing en Sofware que esta desarrollando su proyecto integradora
al cual se le realizo la app en el framework de django y con el cual
se esta llevando a cabo el proyecto
________________________Apps______________________________
se realizo un app para cada una de las partes a utilizar
la lista de apps quedo de la siguiente forma:

 INTEGRADORA
....-app_Cortecaja
........-contenido-de-app

    -app_Dashboard
........-contenido-de-app

    -appcompra
........-contenido-de-app

    -mainapp
........---Pagina Principal---

    -panel_control
........-contenido-de-app


________________________________________________________________________________________

___________________________acomodo interno de las carpetas_____________________________-
se añadio a cada app una ruta definida para que trabajen, no deben de cambiar
se ve de esta manera:

....-app_cortecaja
........-pycache

........-migrations

........-static
............-(carpeta con Nombre de la app)
................-css
................-img <--- esta es para que agreguen si ustedes necesitan img, las otras estan en la bd
................-JS <---- aqui pongan sus archivos el acomodo que usaran es una ruta relativa
            ejemplo:
            ruta relativa--->{% static 'panel_control/css/panel.css' %}

                {% static '(nombre de la carpeta de static)/-css-/-Nombre del archivo css-' %}

            ---esa es la ruta que deben de utilizar tanto para Css como Js si es que hay cambios---

........-templates
................-Aqui van los templates que usaran
____________________________________________________________________________________________________


____________________________Movimientos de las url globales_______________________________
#_____________________MOVIMOS ESTOS_____________________

Tutorial v: aqui van a poner el path que va a tener la vista que se renderiza,

----------1. nombre de la ruta

----------2. llamas a la funcion que hiciste en views.py para que se renderiza

----------3. le asignas un nombre mas este no importa para mas cosas

urlpatterns = [
    path('', views.index, name = 'index'),
    path('compra_venta', views.menu_cv, name='compra_venta'), #Lo movi a appcompra
    path('compra_1', views.compra_1, name = 'compra_1' ), #Lo movi a appcompra
    path('venta_1', views.venta_1, name = 'venta_1'), #Lo movi a appcompra
    path('ajustes_1', views.ajustes_1, name = 'ajustes_1'), se movio a app_caja
    path('dashboard', views.dashboard, name= 'dashboard'), SE MOVIO A DASHBOARD
    path('panel_control', views.panel_control, name= 'panel_control'),
    path('panel_control_personal', views.panel_control_personal, name= 'personal'),
    path('pantalla_carga', views.pantalla_carga, name='pantalla_carga'),
    path('panel_control_transacciones', views.panel_control_transacciones, name='transacciones'),
]

_________________________________urls___________________________________

ejemplo:

from django . urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('panel_control', views.panel_control, name= 'panel_control'),
    path('panel_control_personal', views.panel_control_personal, name= 'personal'),
    path('panel_control_transacciones', views.panel_control_transacciones, name='transacciones'),
]

Es exactamente lo mismo que en sus apps, ya esta hecho pero para que lo tenga en cuenta

_______________________________Views____________________________

from django.shortcuts import render
from mainapp.models import Transaction,Transaction_Details <--agregar esta solo a quine usa la BD


esa es para importar la info de models de la base de datos 
solo debe haber una BD

def panel_control(request):
    return render(request, 'panel.html')

def panel_control_personal(request):
    return render(request, 'personal.html')

def panel_control_transacciones(request):
    return render(request, 'transacciones.html')
_____________________________________________________________________
