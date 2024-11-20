from kaufken.wsgi import *
import os
import django
from app.productos.models import Producto
from django.core.exceptions import ObjectDoesNotExist

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaufken.settings')  # Cambia 'kaufken' por el nombre de tu proyecto
django.setup()

# Eliminar todos los productos de la base de datos
productos = Producto.objects.all()

# Asegúrate de que hay productos en la base de datos antes de intentar eliminarlos
if productos.exists():
    # Eliminar todos los productos
    productos.delete()
    print("Todos los productos fueron eliminados exitosamente.")
else:
    print("No se encontraron productos para eliminar.")
