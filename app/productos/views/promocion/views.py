
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from app.productos.forms import PromocionForm
from app.productos.models import Promocion
from kaufken.mixin import StaffMemberRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin


class PromocionListView(LoginRequiredMixin ,StaffMemberRequiredMixin, ListView):
    model = Promocion
    template_name = "promocion/table.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Promociones'
        context['entity'] = 'Promocion'
        context['create_url'] = reverse_lazy('productos:crearPromociones')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Promocion.objects.all():
                    promocion_data = i.toJSON()
                    promocion_data['estado'] = "✔️" if i.estado else "❌"  # Usar el símbolo correspondiente
                    data.append(promocion_data)
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
             data = {'error': str(error)}
        return JsonResponse(data, safe=False)


class PromocionCreateView(LoginRequiredMixin, StaffMemberRequiredMixin, CreateView):
    model = Promocion
    template_name = "promocion/crear.html"
    form_class = PromocionForm
    success_url = reverse_lazy('productos:listarPromociones')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Promociones'
        context['action'] = 'add'
        context['entity'] = 'Promocion'
        context['list_url'] = self.success_url
        
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                 form = PromocionForm(request.POST, request.FILES)
                 if form.is_valid():
                     promocion = form.save(commit=False)
                     promocion.autor = self.request.user
                     promocion.save()  # Guardamos el producto
                     data['success'] = 'Promocion agregada correctamente'
                 else:
                    data['error'] = form.errors
            else: 
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)


class PromocionUpdateView(LoginRequiredMixin, StaffMemberRequiredMixin, UpdateView):
    model = Promocion
    template_name = "producto/crear.html"
    form_class = PromocionForm
    success_url = reverse_lazy('productos:listarPromociones')  

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Verifica si la acción es 'edit'
            action = request.POST.get('action')
            if action == 'edit':
                form = PromocionForm(request.POST, request.FILES, instance=self.object)
                if form.is_valid():
                    promocion = form.save(commit=False)
                    promocion.autor = self.request.user  # Asigna el autor al producto
                    promocion.save()  # Guarda el producto actualizado
                    data['success'] = 'Promocion actualizada correctamente'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Promociones'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        context['entity'] = 'Promocion'
        return context


class PromocionDeleteView(LoginRequiredMixin, StaffMemberRequiredMixin, DeleteView):
    model = Promocion
    template_name = "promocion/delete.html"
    success_url = reverse_lazy('productos:listarPromociones')  
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['success'] = 'Promocion eliminada correctamente'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Promocion'
        context['list_url'] = self.success_url
        context['entity'] = 'Promocion'
        return context
    
    
    
