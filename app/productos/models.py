from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Deferrable, UniqueConstraint
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
    codigo_qr = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(100)])
    descripcion = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(default="placeholder.png", upload_to='productosImage/', blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.nombre
    
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen'])
        return item
    
    
    class Meta:
        db_table = 'producto'
        # constraints = [
        #     UniqueConstraint(
        #         fields=['codigo_qr'],
        #         name='unique_codigo_qr',
        #         # Deferrable no es compatible con SQLite, así que considera eliminarlo si usas SQLite
        #         # deferrable=Deferrable.DEFERRED,
        #     )
        # ]
