# Generated by Django 5.1.1 on 2024-12-02 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_producto_is_active_alter_producto_autor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='marca',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['-created_at']},
        ),
    ]
