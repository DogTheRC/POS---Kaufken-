from kaufken.wsgi import *
import os
import django
from app.productos.models import *  # Asegúrate de que este sea el nombre correcto de tu aplicación
from faker import Faker
from django.contrib.auth.models import User
from random import choice
from datetime import timedelta
from django.utils import timezone

# Crear una instancia de Faker para generar datos aleatorios
fake = Faker()

# Obtener un autor (usuario) de la base de datos, o puedes especificar un usuario directamente
autor = User.objects.first()  # Si quieres un usuario específico, puedes usar User.objects.get(id=1)

# Verificar si ya existen categorías y marcas, si no, crearlas
categorias = Categoria.objects.all()
marcas = Marca.objects.all()

if not categorias:
    for i in range(5):
        Categoria.objects.create(nombre=f"Categoría {fake.word()}")
    categorias = Categoria.objects.all()

if not marcas:
    for i in range(5):
        Marca.objects.create(nombre=f"Marca {fake.company()}")
    marcas = Marca.objects.all()

# Crear 100 productos aleatorios
for i in range(1, 5000):
    # Generar fechas aleatorias para fecha_elaboracion y fecha_vencimiento
    fecha_elaboracion = fake.date_this_decade(before_today=True, after_today=False)  # Fecha en el pasado
    fecha_vencimiento = fake.date_this_year(before_today=False, after_today=True)  # Fecha en el futuro

    producto = Producto(
        codigo_qr=f'QR{i:03d}',  # El código QR debe ser único, estamos generando uno con un número secuencial
        nombre=f'Producto {i}',
        precio=fake.random_int(min=100, max=10000),  # Precio aleatorio entre 100 y 10,000
        descripcion=fake.sentence(nb_words=10),  # Descripción aleatoria
        stock=fake.random_int(min=0, max=100),  # Stock aleatorio entre 0 y 100
        categoria=choice(categorias),  # Elegir una categoría aleatoria
        marca=choice(marcas),  # Elegir una marca aleatoria
        autor=autor,  # Usar el primer usuario como autor
        fecha_elaboracion=fecha_elaboracion,  # Asignar fecha de elaboración
        fecha_vencimiento=fecha_vencimiento,  # Asignar fecha de vencimiento
    )
    producto.save()

print("productos fueron creados exitosamente.")
