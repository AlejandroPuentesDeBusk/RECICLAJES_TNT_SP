from django.db import models

# Create your models here.
class Material(models.Model):
    #nombre del campo a usar = modelo.CharField es un modelo para que furule
    #y dentro en parentesis la cantidad de caracteres que soporta
    Material_Type = models.CharField(max_length = 100)
    Wholesale_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Wholesale_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)
    #lo de blanck true y null true es para que pueda no haber una imagen en cada registro para no batallar
    #image field checa que si sea un png o jpg y el upload es para que l imagen se valla ahi y no se guarde en bd
    image = models.ImageField(upload_to='img/materiales/', blank=True, null=True)
    #estoy aprendiendo segun la documentacion defino como la llamo
    #asi que hare el def que se autollame y lo muestre
    def __str__(self):#se autocmopleto con el intellicode
        return self.Material_Type

    #segun se ahora deberia hacer una migracion y agregarla