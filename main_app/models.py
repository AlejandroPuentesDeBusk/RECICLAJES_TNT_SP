from django.db import models

# Create your models here.

class Material(models.Model):
    Material_ID = models.AutoField(primary_key=True)
    Material_Type = models.CharField(max_length = 100)
    Stock = models.DecimalField(max_digits=10, decimal_places=2)
    Wholesale_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Wholesale_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Purchase_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Retail_Sale_Price = models.DecimalField(max_digits=10, decimal_places=2)

class Users(models.Model):

    PRIVILEGES = (
        ('admin', 'admin'),
        ('worker', 'worker')
    )
    
    User_ID = models.AutoField(primary_key= True)
    Name = models.CharField(max_length= 100)
    Paternal_Surname = models.CharField(max_length= 100)
    Maternal_Surname = models.CharField(max_length= 100)
    Email = models.EmailField(max_length=100)
    Phone = models.CharField(max_length=50)
    Username = models.CharField(max_length= 100)
    User_Password = models.CharField(max_length=100)
    User_Privileges = models.CharField(max_length= 10, choices = PRIVILEGES, default='worker')

class Day_Report(models.Model):
    Report_ID = models.AutoField(primary_key=True)
    #Start_Time = models.DateTimeField()
    #End_Time = models.DateTimeField()
    #Day = models.DurationField()                  #|Todavía no estoy seguro de
    Day = models.DateField(auto_now_add= True)     #|cómo vamos a guardar las fechas
    Initial_Money = models.DecimalField(max_digits= 10, decimal_places=2)
    Spent = models.DecimalField(max_digits=10, decimal_places=2)
    Obtained = models.DecimalField(max_digits=10, decimal_places=2)
    Final_Money = models.DecimalField(max_digits=10, decimal_places=2)
    Details = models.ManyToManyField(Material, through='Report_Details', related_name='reports')

class Report_Details(models.Model):
    Detail_ID = models.AutoField(primary_key=True)
    Report_ID = models.ForeignKey(Day_Report, on_delete=models.SET_NULL, null=True)
    Material_ID = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    Initial_Stock = models.DecimalField(max_digits=10, decimal_places=2)
    Final_Stock = models.DecimalField(max_digits=10, decimal_places=2)
    Sales_Generated = models.DecimalField(max_digits=10, decimal_places=2)
    Purchases_Spent = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction (models.Model):

    STATUS = (
        ('COMPLETED', 'Completada'),
        ('PENDING', 'Pendiente'),
        ('CANCELED', 'Cancelado'),
    )

    TRANSACTION_TYPES = (
        ('SALE', 'Venta'),
        ('Purchase', 'Compra'),
    )

    Transaction_ID = models.AutoField(primary_key=True)
    User_ID = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    Total = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length= 10,choices= STATUS, default='Completada')
    Transaction_Type = models.CharField(max_length=10,choices= TRANSACTION_TYPES)
    Description = models.CharField(max_length= 100)
    Details = models.ManyToManyField(Material, through='Transaction_Details', related_name='transactions')

class Transaction_Details(models.Model):
    Detail_ID = models.AutoField(primary_key=True)
    Material_ID = models.ForeignKey(Material, on_delete= models.SET_NULL , null=True)
    Transaction_ID = models.ForeignKey(Transaction, on_delete = models.SET_NULL, null=True)
    Price =  models.DecimalField(max_digits=10, decimal_places=2)
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.DecimalField(max_digits= 10, decimal_places= 2)