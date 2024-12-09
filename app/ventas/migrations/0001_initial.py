# Generated by Django 5.1.1 on 2024-11-29 01:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0004_alter_producto_stock_critico_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=130, unique=True)),
                ('saldo_inicial', models.PositiveBigIntegerField(default=0)),
                ('saldo_final', models.PositiveBigIntegerField(default=0)),
                ('cerrado', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('close_at', models.DateTimeField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'caja',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ArqueoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_inicial', models.PositiveIntegerField()),
                ('monto_real', models.PositiveIntegerField()),
                ('fecha_arqueo', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arqueos', to='ventas.caja')),
            ],
            options={
                'db_table': 'arqueo_caja',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('total', models.PositiveIntegerField(default=0)),
                ('metodo_pago', models.CharField(choices=[('EF', 'Efectivo'), ('TD', 'Targeta Debito')], max_length=15)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'venta',
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.PositiveIntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta')),
            ],
            options={
                'db_table': 'detalle_venta',
            },
        ),
    ]
