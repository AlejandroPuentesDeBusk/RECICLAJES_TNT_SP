from django . urls import path
from . import views
from django.contrib.auth import views as auth_views
#from django.conf.urls import handler404


urlpatterns = [
    path('panelcontrol', views.panel_control, name= 'panel_control'),
    path('materiales', views.materiales, name= 'materiales'),
    path('personal', views.personal, name= 'personal'),
    path('transacciones', views.transacciones, name='transacciones'),
    path('cortes', views.cortes, name='cortes')
]

#handler404 = 'mainapp.views.error404'
