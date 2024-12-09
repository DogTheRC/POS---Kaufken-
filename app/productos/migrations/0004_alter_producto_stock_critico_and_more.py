# Generated by Django 5.1.1 on 2024-11-29 01:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_alter_producto_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock_critico',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_maximo',
            field=models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_minimo',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
