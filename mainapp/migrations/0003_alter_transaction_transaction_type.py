# Generated by Django 5.1.3 on 2024-11-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_day_report_alter_material_table_report_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='Transaction_Type',
            field=models.CharField(choices=[('SALE', 'Venta'), ('PURCHASE', 'Compra'), ('INVESTMENT', 'Inversión'), ('EXPENSE', 'Gasto')], max_length=10),
        ),
    ]
