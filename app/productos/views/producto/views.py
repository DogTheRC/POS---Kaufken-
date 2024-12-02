
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from app.productos.forms import ProductoForm
from app.productos.models import Producto

@method_decorator(staff_member_required, name='dispatch')
class ProductoListView(ListView):
    model = Producto
    template_name = "producto/inventario.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['entity'] = 'Producto'
        context['create_url'] = reverse_lazy('productos:crearProductos')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Producto.objects.all():
                    product_data = i.toJSON()
                    product_data['is_active'] = "✔️" if i.is_active else "❌"  # Usar el símbolo correspondiente
                    data.append(product_data)
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
             data = {'error': str(error)}
        return JsonResponse(data, safe=False)

@method_decorator(staff_member_required, name='dispatch')
class ProductoCreateView(CreateView):
    model = Producto
    template_name = "producto/crear.html"
    form_class = ProductoForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Producto'
        context['action'] = 'add'
        context['entity'] = 'Producto'
        context['list_url'] = self.success_url
        
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                 form = ProductoForm(request.POST, request.FILES)
                 if form.is_valid():
                     producto = form.save(commit=False)
                     producto.autor = self.request.user
                     producto.save()  # Guardamos el producto
                     data['success'] = 'Producto agregado correctamente'
                 else:
                    data['error'] = form.errors
            else: 
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)

@method_decorator(staff_member_required, name='dispatch')
class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = "producto/crear.html"
    form_class = ProductoForm
    success_url = reverse_lazy('productos:listarProductos')  

    def get_object(self, queryset=None):
        codigo_barra = self.kwargs.get('codigo_barra')  
        return get_object_or_404(Producto, codigo_barra=codigo_barra) 

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Verifica si la acción es 'edit'
            action = request.POST.get('action')
            if action == 'edit':
                form = ProductoForm(request.POST, request.FILES, instance=self.object)
                if form.is_valid():
                    producto = form.save(commit=False)
                    print(producto)
                    producto.autor = self.request.user  # Asigna el autor al producto
                    producto.save()  # Guarda el producto actualizado
                    data['success'] = 'Producto actualizado correctamente'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        context['entity'] = 'Producto'
        return context

@method_decorator(staff_member_required, name='dispatch') 
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "producto/delete.html"
    success_url = reverse_lazy('productos:listarProductos')  
    
    def get_object(self, queryset=None):
        codigo_barra = self.kwargs.get('codigo_barra')  
        return get_object_or_404(Producto, codigo_barra=codigo_barra) 
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['success'] = 'Producto eliminado correctamente'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Producto'
        context['list_url'] = self.success_url
        context['entity'] = 'Producto'
        return context