# Generated by Django 5.1.1 on 2024-12-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='tipo',
            field=models.CharField(choices=[('stock_minimo', 'Producto en stock minimo'), ('stock_critico', 'Producto en stock critico'), ('sin_stock', 'Producto sin stock'), ('fecha_vencimiento', 'Producto cerca de Fecha de Vencimiento'), ('producto_vencido', 'Producto Vencido'), ('comentario', 'Comentario')], max_length=50),
        ),
    ]
