from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'categoria'

class Marca(models.Model):
    nombre = models.CharField(max_length=150) 
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'marca'

class Producto(models.Model):
    codigo_qr = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(100)])
    descripcion = models.CharField(max_length=300, blank=True)
    imagen = models.ImageField(default="placeholder.png", upload_to='productosImage/', blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.nombre
    
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen'])
        return item
    def delete(self, *args, **kwargs):
        # Actualizamos la fecha de eliminación en las fechas asociadas antes de eliminar el producto
        self.fechas.update(deleted_at=timezone.now())  
        super(Producto, self).delete(*args, **kwargs)  # Ahora se llama al método delete original
    
    class Meta:
        db_table = 'producto'
        
class FechaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, related_name='fechas')
    fecha_elaboracion = models.DateField()
    fecha_vencimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de la última modificación
    deleted_at = models.DateTimeField(null=True, blank=True)  # Fecha de eliminación

    def __str__(self):
        return f"Fechas de {self.producto.nombre}"
    
    def clean(self):
        if self.fecha_elaboracion and self.fecha_vencimiento:
            if self.fecha_elaboracion > self.fecha_vencimiento:
                raise ValidationError('La fecha de elaboración no puede ser mayor que la fecha de vencimiento.')
        super().clean()

    class Meta:
        db_table = 'fecha_producto'