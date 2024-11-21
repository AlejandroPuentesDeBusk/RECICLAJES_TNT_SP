from django import forms
from .models import Material
#SE CREO UN MODELO DE FORMULARIO
#para hacer mas rapido el trabajar con el form y no batallar

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['Material_Type', 'Wholesale_Purchase_Price', 'Wholesale_Sale_Price', 'Retail_Purchase_Price', 'Retail_Sale_Price', 'image']
