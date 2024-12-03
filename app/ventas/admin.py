from django.contrib import admin
from app.ventas.models import Pago, Venta, DetalleVenta

# Register your models here.
admin.site.register(Venta)
admin.site.register(Pago)
admin.site.register(DetalleVenta)
