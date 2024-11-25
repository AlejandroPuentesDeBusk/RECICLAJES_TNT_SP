from django . urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404




urlpatterns = [
    path('compra_venta', views.menu_cv, name='compra_venta'),
    path('compra_1', views.compra_1, name = 'compra_1' ),
    path('venta_1', views.venta_1, name = 'venta_1'),
    path('cv', views.cv, name= 'cv'),
    path('com_ven', views.com_ven, name= 'com_ven'),
    ]

