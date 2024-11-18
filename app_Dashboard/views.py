from django.shortcuts import render



# Create your views here.
#request de francisco
#@login_required
def dashboard(request):
    return render(request, 'dashboard.html')