from django . urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404




urlpatterns = [
    path('cv', views.cv, name= 'cv'),
    ]

