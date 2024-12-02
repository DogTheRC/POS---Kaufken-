
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from app.ventas.models import DetalleVenta
from django.views.generic import CreateView, ListView, DeleteView, FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@method_decorator(staff_member_required, name='dispatch')
class DetalleListView(ListView):
    model = DetalleVenta
    template_name = "detalle_venta/table.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registros de Detalles Ventas'
        context['entity'] = 'Detalle Venta'
        context['create_url'] = reverse_lazy('ventas:crearVentas')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in DetalleVenta.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
             data = {'error': str(error)}
        return JsonResponse(data, safe=False)