from django . urls import path
from . import views
from django.contrib.auth import views as auth_views

#tutorial v: aqui van a poner el path que va a tener la vista que se renderiza,
#1. nombre de la ruta
#2. llamas a la funcion que hiciste en views.py para que se renderiza
#3. le asignas un nombre mas este no importa para mas cosas

urlpatterns = [
    path('', views.index, name = 'index'),
    path('compra_1', views.compra_1, name = 'compra_1' ),
    path('venta_1', views.venta_1, name = 'venta_1'),
    path('ajustes_1', views.ajustes_1, name = 'ajustes_1'),
    path('dashboard', views.dashboard, name= 'dashboard'),
    path('panel_control', views.panel_control, name= 'panel_control'),
    path('panel_control_personal', views.panel_control_personal, name= 'personal'),
    path('pantalla_carga', views.pantalla_carga, name='pantalla_carga')
]