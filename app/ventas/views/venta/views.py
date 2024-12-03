import json
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from app.ventas.forms import VentaForm, DetalleVentaForm, PagoForm
from app.productos.models import Producto
from app.ventas.models import Venta, DetalleVenta, Pago
from django.db.models import Q
from django.db import transaction
from django.views.generic import CreateView, ListView, DeleteView

from kaufken.mixin import StaffMemberRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class VentaView(LoginRequiredMixin, CreateView):
    template_name = "venta/venta.html"
    form_class = VentaForm
    success_url = reverse_lazy('')  
    def get(self, request, *args, **kwargs):
        venta_form = VentaForm()
        detalle_form = DetalleVentaForm()
        pago_form = PagoForm()
        context = {
            'venta_form': venta_form,
            'detalle_form': detalle_form,
            'pago_form': pago_form,
            'action': 'add',
            'title': 'Registrar Venta',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'add':
                with transaction.atomic():
                    
                    ventas = json.loads(request.POST['ventas'])
                    venta = Venta()
                    
                    user = self.request.user
                    venta.usuario = user
         
                    venta.total = ventas['total']
                    venta.save()
                    
                    for i in ventas['productos']:
                        detalle = DetalleVenta() 
                        detalle.venta = venta
                        detalle.producto = Producto.objects.get(id=i['id'])
                        detalle.cantidad = int(i['cantidad'])
                        detalle.precio_unitario = float(i['precio'])
                        detalle.save()
                        detalle.producto.stock -= detalle.cantidad
                        detalle.producto.save()
                        
                    for i in ventas['pagos']:
                        pago = Pago()
                        pago.venta = venta
                        pago.monto = i['monto']
                        pago.metodo_pago = i['metodo_pago']
                        pago.save()
                        data['success'] = 'Venta, detalle y pago registrados correctamente'
                        
            elif action == 'autocomplete':
                data = {'results': []}
                ids_exclude = json.loads(request.POST['ids'])     
                # Filtrar productos por el término de búsqueda y asegurarse de que el stock sea mayor que 0
                productos = Producto.objects.filter(
                    Q(nombre__icontains=request.POST['term']) | Q(codigo_barra__icontains=request.POST['term']),
                    stock__gt=0  # Asegurarse de que el stock sea mayor que 0
                ).exclude(id__in=ids_exclude).exclude(is_active=False)[:10]  # Limitar a los primeros 10 productos
                for i in productos:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    item['imagen'] = i.imagen.url if i.imagen else None
                    item['categoria'] = i.categoria.nombre if i.categoria else None
                    item['marca'] = i.marca.nombre if i.marca else None
                    item['codigo_barra'] = i.codigo_barra if i.codigo_barra else None
                    item['precio'] = i.precio if i.precio else None
                    data['results'].append(item) 
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False) 


class VentaListView(LoginRequiredMixin, StaffMemberRequiredMixin, ListView):
    model = Venta
    template_name = "venta/table.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registros de Ventas'
        context['entity'] = 'Venta'
        context['create_url'] = reverse_lazy('ventas:crearVentas')
        return context

    def post(self, request, *args, **kwargs):
        data = []
        action = request.POST.get('action', '')
        try:
            if action == 'search':
                ventas = Venta.objects.all()  # Obtener todas las ventas
                for venta in ventas:
                    venta_data = venta.toJSON()  # Obtener datos de la venta
                    # Obtener los detalles de la venta
                    detalles = DetalleVenta.objects.filter(venta=venta)
                    venta_data['detalles'] = [detalle.toJSON() for detalle in detalles]
                    # Obtener los pagos asociados a la venta
                    pagos = Pago.objects.filter(venta=venta)
                    venta_data['pagos'] = [pago.toJSON() for pago in pagos]
                    data.append(venta_data)
            else:
                data = {'error': 'No se ha ingresado ninguna acción.'}
        except Exception as error:
            data = {'error': str(error)}
        return JsonResponse(data, safe=False)
    

class VentaDeleteView(LoginRequiredMixin, StaffMemberRequiredMixin, DeleteView):
    model = Venta
    template_name = "venta/delete.html"
    success_url = reverse_lazy('ventas:listarVentas')  
       
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['success'] = 'Categoria eliminada correctamente'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Ventas'
        context['list_url'] = self.success_url
        context['entity'] = 'Venta'
        return context