# Generated by Django 5.1.1 on 2024-10-09 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_producto_unique_codigo_qr_alter_producto_table'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='producto',
            name='unique_codigo_qr',
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo_qr',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterModelTable(
            name='producto',
            table='producto',
        ),
    ]
