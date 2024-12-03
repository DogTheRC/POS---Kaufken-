from django.db import models
from django.contrib.auth.models import User
from app.productos.models import Producto, Promocion
from decimal import Decimal
from django.forms.models import model_to_dict
from app.ventas.validation import *


class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)

    def calcular_total(self):
        # Calcula el total sumando los subtotales de los detalles
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()
        
    def toJSON(self):
        item = model_to_dict(self)
        item['usuario_nombre'] = self.usuario.username if self.usuario else "Desconocida"
        item['create_at'] = self.create_at.strftime('%d-%m-%Y %H:%M')
        return item

    def delete(self, using=None, keep_parents=False):
        # Ajuste del stock de los productos antes de eliminar la venta
        for detalle in self.detalles.all():  # Usamos 'self.detalles.all()' que es más eficiente
            detalle.producto.stock += detalle.cantidad  # Aumentar el stock del producto
            detalle.producto.save()  # Guardamos el producto actualizado
        super(Venta, self).delete(using=using, keep_parents=keep_parents)  # Eliminamos la venta

    def clean(self):
        validate_venta(self)
    def __str__(self):
        return f"Venta {self.id} - Usuario: {self.usuario}"

    class Meta:
        db_table = 'venta'
        ordering = ['-create_at']
        

class Pago(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    METODO_PAGOS = [
        ('EF', 'Efectivo'),
        ('TD', 'Tarjeta Débito'),
    ]
    metodo_pago = models.CharField(max_length=15, choices=METODO_PAGOS)
    monto = models.PositiveIntegerField()
    fecha_pago = models.DateTimeField(auto_now_add=True)
    es_pago_parcial = models.BooleanField(default=False)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_pago'] = self.fecha_pago.strftime('%d-%m-%Y %H:%M')
        return item

    def __str__(self):
        return f"Pago {self.id} - Venta: {self.venta.id} - Monto: {self.monto}"
    
    def clean(self):
        validate_pago(self)

    class Meta:
        db_table = 'pago'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    descuento_aplicado = models.PositiveIntegerField(default=0) # Descuento manual adicional
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Calcular el subtotal antes de guardar
        self.subtotal = Decimal(self.cantidad) * Decimal(self.precio_unitario)
        super().save(*args, **kwargs)
    def toJSON(self):
        item = model_to_dict(self)
        item['producto_nombre'] = self.producto.nombre if self.producto else "Desconocida"
        return item
    
    def clean(self):
        validate_detalle_venta(self) 
    def __str__(self):
        return f"Detalle {self.id} - Venta: {self.venta.id}"
    
    class Meta:
        db_table = 'detalle_venta'


class Caja(models.Model):
    nombre = models.CharField(max_length=130, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    saldo_inicial = models.PositiveBigIntegerField(default=0)
    saldo_final = models.PositiveBigIntegerField(default=0)  # Cambiado a PositiveBigIntegerField para consistencia
    cerrado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    close_at = models.DateTimeField(null=True, blank=True)  # Permite nulos si no está cerrada aún

    class Meta:
        db_table = 'caja'
        ordering = ['-created_at']

    def __str__(self):
        return f"Caja {self.nombre} - {self.created_at}"


class ArqueoCaja(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='arqueos')
    monto_inicial = models.PositiveIntegerField()
    monto_real = models.PositiveIntegerField()
    fecha_arqueo = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def diferencia(self):
        return self.monto_real - self.monto_inicial

    class Meta:
        db_table = 'arqueo_caja'

    def __str__(self):
        return f"Arqueo {self.id} - Caja: {self.caja.nombre}"
