from django.db import models
from django.forms.models import model_to_dict
from app.productos.models import Producto
from app.users.models import User

# Create your models here.
class Notificacion(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=150)
    TIPO_CHOICES = [
        ('stock_minimo', 'Producto en stock minimo'),
        ('stock_critico', 'Producto en stock critico'),
        ('sin_stock', 'Producto sin stock'),
        ('fecha_vencimiento', 'Producto cerca de Fecha de Vencimiento'),
        ('producto_vencido', 'Producto Vencido'),
        ('comentario', 'Comentario'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    leido = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['producto_nombre'] = self.producto.nombre if self.producto else None 
        item['producto_stock'] = self.producto.stock if self.producto else None 
        item['usuario_nombre'] = self.usuario.username if self.usuario else None
        item['created_at'] = self.created_at.strftime('%d-%m-%Y %H:%M')
        return item
    def __str__(self):
        return f"{self.titulo} - {self.producto.nombre}"
    
    class Meta:
        db_table = 'notificacion'

