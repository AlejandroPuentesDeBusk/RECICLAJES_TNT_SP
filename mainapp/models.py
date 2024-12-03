from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Material(models.Model):
    Material_Type = models.CharField(
        max_length=100, 
        verbose_name=_("Tipo de Material")
    )
    Wholesale_Purchase_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Precio de Compra al Mayoreo")
    )
    Wholesale_Sale_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Precio de Venta al Mayoreo")
    )
    Retail_Purchase_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Precio de Compra al Menudeo")
    )
    Retail_Sale_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Precio de Venta al Menudeo")
    )
    image = models.ImageField(
        upload_to='img/materiales/', 
        blank=True, 
        null=True, 
        verbose_name=_("Imagen")
    )

    class Meta:
        db_table = 'mainapp_material'
        verbose_name = _("Material")
        verbose_name_plural = _("Materiales")

    @property 
    def Stock(self):
        purchases = Transaction_Details.objects.filter(
            Material=self, 
            Transaction__Transaction_Type='PURCHASE'
        ).aggregate(
            total_purchased=models.Sum('Quantity')
        )['total_purchased'] or 0

        sales = Transaction_Details.objects.filter(
            Material=self, 
            Transaction__Transaction_Type='SALE'
        ).aggregate(
            total_sold=models.Sum('Quantity')
        )['total_sold'] or 0

        return purchases - sales
    
    def __str__(self):
        return self.Material_Type

class Users(AbstractUser):
    first_name = None #Es para que no se generen estos campos
    last_name = None

    Name = models.CharField(
        max_length=100,
        verbose_name=_("Nombre")
    )
    Paternal_Surname = models.CharField(
        max_length=100,
        verbose_name=_("Apellido Paterno")
    )
    Maternal_Surname = models.CharField(
        max_length=100,
        verbose_name=_("Apellido Materno")
    )
    Phone = models.CharField(
        max_length=50,
        verbose_name=_("Teléfono")
    )

class Transaction (models.Model):

    STATUS = (
        ('COMPLETED', _('Completada')),
        ('PENDING', _('Pendiente')),
        ('CANCELED', _('Cancelada')),
    )

    TRANSACTION_TYPES = (
        ('SALE', _('Venta')),
        ('PURCHASE', _('Compra')),
        ('INVESTMENT', _('Inversión')),
        ('EXPENSE', _('Gasto')),
    )

    User = models.ForeignKey(
        'Users', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Usuario")
    )
    Total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Total")
    )
    Discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,  
        null=True,
        verbose_name=_("Descuento")
    )
    Date = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Fecha")
    )
    Status = models.CharField(
        max_length=10, 
        choices=STATUS, 
        default='COMPLETED',
        verbose_name=_("Estado")
    )
    Transaction_Type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES,
        verbose_name=_("Tipo de Transacción")
    )
    Description = models.CharField(
        max_length=100,
        verbose_name=_("Descripción")
    )
    Details = models.ManyToManyField(
        'Material', 
        through='Transaction_Details', 
        related_name='transactions',
        verbose_name=_("Detalles")
    )
    
    class Meta:
        verbose_name = _("Transacción")
        verbose_name_plural = _("Transacciones")

    def __str__(self):
        return f"{self.get_Transaction_Type_display()} hecha por {self.User.username if self.User else 'Usuario Desconocido'}"

class Transaction_Audit(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=20)
    log_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Action} {self.Transaction_Type} {self.Log_Date}"

class Transaction_Details(models.Model):
    Material = models.ForeignKey(
        'Material', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Material")
    )
    Transaction = models.ForeignKey(
        'Transaction', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Transacción")
    )
    Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Precio")
    )
    Subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Subtotal")
    )
    Quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Cantidad")
    )

    class Meta:
        verbose_name = _("Detalle de Transacción")
        verbose_name_plural = _("Detalles de Transacciones")

    def __str__(self):
        return f"Detalle de {self.Transaction.Transaction_Type} - {self.Transaction.id if self.Transaction else 'N/A'}"

class Day_Report(models.Model):
    Day = models.DateField(
        auto_now_add=True,
        verbose_name=_("Día")
    )
    Initial_Money = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Dinero Inicial")
    )
    Spent = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Gastado")
    )
    Obtained = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Obtenido")
    )
    Final_Money = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Dinero Final")
    )
    Details = models.ManyToManyField(
        'Material', 
        through='Report_Details', 
        related_name='reports',
        verbose_name=_("Detalles")
    )

    class Meta:
        verbose_name = _("Reporte Diario")
        verbose_name_plural = _("Reportes Diarios")

    def __str__(self):
        return f"Reporte del {self.Day} - {self.id}"

class Report_Details(models.Model):
    Report_ID = models.ForeignKey(
        'Day_Report', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Reporte")
    )
    Material_ID = models.ForeignKey(
        'Material', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Material")
    )
    Initial_Stock = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Inventario Inicial")
    )
    Final_Stock = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Inventario Final")
    )
    Sales_Generated = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Ventas Generadas")
    )
    Purchases_Spent = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("Compras Gastadas")
    )

    class Meta:
        verbose_name = _("Detalle del Reporte")
        verbose_name_plural = _("Detalles de Reportes")

    def __str__(self):
        return f"Detalles del reporte del {self.Report_ID.Day} - {self.Report_ID.id if self.Report_ID else 'N/A'}"