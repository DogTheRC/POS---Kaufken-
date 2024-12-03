from .models import Categoria, Marca, Producto, Promocion
from django import forms



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_barra','nombre', 'precio', 'descripcion', 'imagen', 'stock','stock_critico','stock_minimo','stock_maximo', 'categoria', 'marca','promocion','fecha_elaboracion', 'fecha_vencimiento','is_active']
        widgets = {
            'codigo_barra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Barras'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock'}), 
            'stock_critico': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock crítico: cantidad que activa la alerta si está por debajo', 'value': 5}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock mínimo: cantidad mínima para satisfacer la demanda', 'value': 10}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock máximo: cantidad máxima que puedes almacenar', 'value': 50}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'promocion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_elaboracion': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date', 'required':'required'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'is_active': 'Producto Activo',  # Aquí se cambia el nombre del campo a "Producto Activo"
        }


class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'descuento', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la promoción'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la promoción', 'rows': 3}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descuento en porcentaje', 'min': 0, 'max': 100}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'estado': 'Promoción activa',
            'autor': 'Autor de la promoción', 
        }

        