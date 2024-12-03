from django import forms
from django.forms import modelformset_factory
from .models import Transaction, Transaction_Details, Material, Users
from django.contrib.auth.forms import PasswordChangeForm


class loginn(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'}))

# MODELFORMS PARA ESTILOS CREACION Y ACTUALIZACIÓN ------------------------------------------------------------
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['Material_Type', 'Wholesale_Purchase_Price', 'Wholesale_Sale_Price', 
                  'Retail_Purchase_Price', 'Retail_Sale_Price', 'image']
        widgets = {
            'Material_Type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Material'}),
            'Wholesale_Purchase_Price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Compra al Mayoreo'}),
            'Wholesale_Sale_Price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Venta al Mayoreo'}),
            'Retail_Purchase_Price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Compra al Menudeo'}),
            'Retail_Sale_Price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de Venta al Menudeo'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'Name', 'Paternal_Surname', 'Maternal_Surname', 
                  'Phone', 'is_superuser', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'Paternal_Surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'Maternal_Surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'Name', 'Paternal_Surname', 'Maternal_Surname', 'Phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'Paternal_Surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'Maternal_Surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario personalizado para cambiar contraseña."""
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['User', 'Total', 'Discount', 'Status', 'Transaction_Type', 'Description']
        widgets = {
            'User': forms.Select(attrs={'class': 'form-control'}),
            'Total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total'}),
            'Discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
            'Status': forms.Select(attrs={'class': 'form-control'}),
            'Transaction_Type': forms.Select(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # para update el total se hace solo de lectura
        if self.instance and self.instance.pk:
            self.fields['Total'].widget.attrs['readonly'] = True