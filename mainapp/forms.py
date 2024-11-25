from django import forms
from .models import Transaction, Transaction_Details

class loginn(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'}))