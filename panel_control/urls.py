from django . urls import path
from . import views
from django.contrib.auth import views as auth_views
#from django.conf.urls import handler404


urlpatterns = [
    path('panel_control', views.panel_control, name= 'panel_control'),
    path('panel_control_personal', views.panel_control_personal, name= 'personal'),
    path('panel_control_transacciones', views.panel_control_transacciones, name='transacciones'),
]

#handler404 = 'mainapp.views.error404'
