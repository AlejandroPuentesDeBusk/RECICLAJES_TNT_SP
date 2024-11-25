from django.contrib import admin
from .models import Material, Users, Transaction, Transaction_Details, Day_Report, Report_Details

# Register your models here.

admin.site.register(Material)
admin.site.register(Users)
admin.site.register(Transaction)
admin.site.register(Transaction_Details)
admin.site.register(Day_Report)
admin.site.register(Report_Details)