from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from mainapp.models import Material, Transaction
from django.utils import timezone

# Create your views here.


#@login_required
def ajustes_1(request):
    return render(request, 'ajustes_1.html')

