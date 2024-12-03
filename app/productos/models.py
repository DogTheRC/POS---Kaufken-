from django.db import models
from app.productos.validation import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de la última modificación
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['autor_nombre'] = self.autor.username if self.autor else None
        item['created_at'] = self.created_at.strftime('%d-%m-%Y %H:%M')
        item['update_at'] = self.updated_at.strftime('%d-%m-%Y %H:%M')
        return item
    
    def clean(self):
        validar_nombre_general(self.nombre, tipo="categoría")
        super().clean()
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'categoria'

    
class Marca(models.Model):
    nombre = models.CharField(max_length=150,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)    
    def __str__(self):
        return self.nombre
    def toJSON(self):
        item = model_to_dict(self)
        item['autor_nombre'] = self.autor.username if self.autor else None
        item['created_at'] = self.created_at.strftime('%d-%m-%Y %H:%M')
        item['update_at'] = self.updated_at.strftime('%d-%m-%Y %H:%M')
        return item
    def clean(self):
        validar_nombre_general(self.nombre, tipo="marca")
        super().clean()
    class Meta:
        ordering = ['-created_at']
        db_table = 'marca'
        
        
        
        
 

class Promocion(models.Model):
    
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])  # Descuento en porcentaje
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.BooleanField(default=False)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['autor_nombre'] = self.autor.username if self.autor else None
        item['created_at'] = self.created_at.strftime('%d-%m-%Y %H:%M')
        item['updated_at'] = self.updated_at.strftime('%d-%m-%Y %H:%M')
        item['fecha_inicio'] = self.fecha_inicio.strftime('%d-%m-%Y')
        item['fecha_fin'] = self.fecha_fin.strftime('%d-%m-%Y')
        return item
    
    def clean(self):
        # Validar el nombre de la promoción
       validar_nombre_general(self.nombre, tipo="promocion")
        
        # Validar las fechas
       validar_fechas_promocion(self.fecha_inicio, self.fecha_fin)

        # Validar que el descuento esté en el rango de 0 a 100
       if self.descuento < 0 or self.descuento > 100:
            raise ValidationError('El descuento debe ser un valor entre 0 y 100.')


    class Meta:
        db_table = 'promocion'
        ordering = ['-fecha_inicio']       
        
        
        

# Modelo de Producto
class Producto(models.Model):
    # Campo para el código de barras
    codigo_barra = models.CharField(
        max_length=13,  # Max length suficiente para EAN-13
        unique=True,
        validators=[validar_codigo_barra]  # Agregar el validador
    )
    is_active = models.BooleanField(default=True)
    nombre = models.CharField(max_length=150, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(100)])
    descripcion = models.CharField(max_length=300, blank=True)
    imagen = models.ImageField(default="placeholder.png", upload_to='productosImage/', blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    stock_critico = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(100)])
    stock_minimo = models.PositiveIntegerField(default=2, validators=[MinValueValidator(2),MaxValueValidator(100)])
    stock_maximo = models.PositiveIntegerField(default=3, validators=[MinValueValidator(3),MaxValueValidator(100)])
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_elaboracion = models.DateField()
    fecha_vencimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de la última modificación
    
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def __str__(self):
        return self.nombre
    def toJSON(self):
        item = model_to_dict(self)
        
        nombre_producto = generar_nombre_producto(self.categoria, self.marca, self.nombre, self.descripcion, self.codigo_barra)
        item['nombre'] = nombre_producto
        item['categoria_nombre'] = self.categoria.nombre if self.categoria else "Desconocida"
        item['marca_nombre'] = self.marca.nombre if self.marca else "Desconocida"
        item['autor_nombre'] = self.autor.username if self.autor else "Desconocido"
        item['created_at'] = self.created_at.strftime('%d-%m-%Y %H:%M')
        item['update_at'] = self.updated_at.strftime('%d-%m-%Y %H:%M')        
        if self.imagen:
            item['imagen'] = self.imagen.url

        return item

    
    
    def clean(self):
        
        # Validación del nombre
        validar_nombre_general(self.nombre, tipo="producto")

        # Validación de las fechas de elaboración y vencimiento
        validar_fechas(self.fecha_elaboracion, self.fecha_vencimiento)

        # Llamar a la función de validación personalizada
        validar_stock(self.stock, self.stock_minimo, self.stock_maximo, self.stock_critico)

        super().clean()
    
    class Meta:
        db_table = 'producto'
        ordering = ['-created_at']
        
