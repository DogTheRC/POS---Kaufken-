from .models import Categoria, Marca, Producto, FechaProducto
from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError


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
        fields = ['codigo_qr','nombre', 'precio', 'descripcion', 'imagen', 'stock', 'categoria', 'marca']
        widgets = {
            'codigo_qr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código QR'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
        }
        
class FechaProductoForm(forms.ModelForm):
    class Meta:
        model = FechaProducto
        fields = ['fecha_elaboracion', 'fecha_vencimiento']
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required':'required'}),
        }


FechaProductoFormset = forms.inlineformset_factory(
    Producto, FechaProducto, form=FechaProductoForm, extra=1, can_delete=False
)