from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Material(models.Model):
    Material_Type = models.CharField(max_length = 100)
    Wholesale_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Wholesale_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)
    #lo de blanck true y null true es para que pueda no haber una imagen en cada registro para no batallar
    #image field checa que si sea un png o jpg y el upload es para que l imagen se valla ahi y no se guarde en bd
    image = models.ImageField(upload_to='img/materiales/', blank=True, null=True)


    @property 
    def Stock(self):
        purchases = Transaction_Details.objects.filter(Material = self, Transaction__Transaction_Type = 'PURCHASE').aggregate(total_purchased = models.Sum('Quantity'))['total_purchased'] or 0
        
        sales = Transaction_Details.objects.filter(Material = self, Transaction__Transaction_Type = 'SALE').aggregate(total_sold = models.Sum('Quantity'))['total_sold'] or 0
        
        return purchases - sales

class Users(AbstractUser):
    first_name = None #Es para que no se generen estos campos
    last_name = None

    Name = models.CharField(max_length= 100)
    Paternal_Surname = models.CharField(max_length= 100)
    Maternal_Surname = models.CharField(max_length= 100)
    Phone = models.CharField(max_length=50)

class Transaction (models.Model):

    STATUS = (
        ('COMPLETED', 'Completada'),
        ('PENDING', 'Pendiente'),
        ('CANCELED', 'Cancelado'),
    )

    TRANSACTION_TYPES = (
        ('SALE', 'Venta'),
        ('PURCHASE', 'Compra'),
    )

    User = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Total = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length= 10,choices= STATUS, default='Completada')
    Transaction_Type = models.CharField(max_length=10,choices= TRANSACTION_TYPES)
    Description = models.CharField(max_length= 100)
    Details = models.ManyToManyField(Material, through='Transaction_Details', related_name='transactions')

class Transaction_Details(models.Model):
    Material = models.ForeignKey(Material, on_delete= models.SET_NULL , null=True)
    Transaction = models.ForeignKey(Transaction, on_delete = models.SET_NULL, null=True)
    Price =  models.DecimalField(max_digits=10, decimal_places=2)
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.DecimalField(max_digits= 10, decimal_places= 2)