
from django.http import  JsonResponse

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.productos.forms import CategoriaForm
from app.productos.models import Categoria

from kaufken.mixin import StaffMemberRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin


class CategoriaListView(LoginRequiredMixin, StaffMemberRequiredMixin,ListView):
    model = Categoria
    template_name = "categoria/table.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorias'
        context['entity'] = 'Categoria'
        context['create_url'] = reverse_lazy('productos:crearCategorias')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data, safe=False)


class CategoriaCreateView(LoginRequiredMixin, StaffMemberRequiredMixin, CreateView):
    model = Categoria
    template_name = "categoria/crear.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('productos:listarCategorias')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Categorias'
        context['action'] = 'add'
        context['entity'] = 'Categoria'
        context['list_url'] = self.success_url
        
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                 form = CategoriaForm(request.POST, request.FILES)
                 if form.is_valid():
                     categoria = form.save(commit=False)
                     categoria.autor = self.request.user
                     categoria.save()  
                     data['success'] = 'Categoria agregado correctamente'
                 else:
                    data['error'] = form.errors
            else: 
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)

class CategoriaUpdateView(LoginRequiredMixin, StaffMemberRequiredMixin, UpdateView):
    model = Categoria
    template_name = "categoria/crear.html"
    form_class = CategoriaForm
    success_url = reverse_lazy('productos:listarCategorias')  


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Verifica si la acción es 'edit'
            action = request.POST.get('action')
            if action == 'edit':
                form = CategoriaForm(request.POST, request.FILES, instance=self.object)
                if form.is_valid():
                    categoria = form.save(commit=False)
                    categoria.autor = self.request.user  # Asigna el autor al producto
                    categoria.save()  # Guarda el producto actualizado
                    data['success'] = 'Categoria actualizado correctamente'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        context['entity'] = 'Categoria'
        return context


class CategoriaDeleteView(LoginRequiredMixin, StaffMemberRequiredMixin, DeleteView):
    model = Categoria
    template_name = "categoria/delete.html"
    success_url = reverse_lazy('productos:listarCategorias')  
       
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
        context['title'] = 'Eliminar Categoria'
        context['list_url'] = self.success_url
        context['entity'] = 'Categoria'
        return context