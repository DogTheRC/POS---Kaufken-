from django import forms
from app.ventas.models import Venta, DetalleVenta, Pago
from app.productos.models import Producto
from django.forms import ModelChoiceField, Select
from django.utils.timezone import localtime

class VentaForm(forms.ModelForm):
    total = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',  
        }),
        label='Total de la Venta',
    )

    class Meta:
        model = Venta
        fields = ['total']  # Eliminamos metodo_pago ya que ahora está en Pago

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Si la instancia ya existe
            self.fields['total'].initial = self.instance.total


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'monto']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto del pago'}),
        }
        labels = {
            'metodo_pago': 'Método de Pago',
            'monto': 'Monto',
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None:
            if monto <= 0:
                raise forms.ValidationError("El monto debe ser un número entero positivo.")
            if monto != int(monto):  # Verifica que sea un entero
                raise forms.ValidationError("El monto debe ser un número entero.")
        return monto


class DetalleVentaForm(forms.ModelForm):
    search = ModelChoiceField(
        queryset=Producto.objects.none(),
        widget=Select(attrs={
            'class': 'form-control select2',
            'placeholder': 'Buscar Producto...',
        })     
    )

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario'}),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
        }