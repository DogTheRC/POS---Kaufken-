from .models import Categoria, Marca, Producto
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
        fields = ['codigo_qr','nombre', 'precio', 'descripcion', 'imagen', 'stock', 'categoria', 'marca','fecha_elaboracion', 'fecha_vencimiento']
        widgets = {
            'codigo_qr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código QR'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'fecha_elaboracion': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date', 'required':'required'}),
        }
        