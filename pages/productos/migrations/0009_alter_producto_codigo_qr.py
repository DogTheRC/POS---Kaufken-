# Generated by Django 5.1.2 on 2024-10-16 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_remove_producto_unique_codigo_qr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo_qr',
            field=models.CharField(max_length=255),
        ),
    ]