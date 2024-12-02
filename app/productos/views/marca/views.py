
from django.contrib.admin.views.decorators import staff_member_required
from django.http import  JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.productos.forms import MarcaForm
from app.productos.models import Marca

@method_decorator(staff_member_required, name='dispatch')
class MarcaListView(ListView):
    model = Marca
    template_name = "marca/table.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['entity'] = 'Marca'
        context['create_url'] = reverse_lazy('productos:crearMarcas')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Marca.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data, safe=False)

@method_decorator(staff_member_required, name='dispatch')
class MarcaCreateView(CreateView):
    model = Marca
    template_name = "marca/crear.html"
    form_class = MarcaForm
    success_url = reverse_lazy('productos:listarMarcas')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Marcas'
        context['action'] = 'add'
        context['entity'] = 'Marca'
        context['list_url'] = self.success_url
        
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                 form = MarcaForm(request.POST, request.FILES)
                 if form.is_valid():
                     marca = form.save(commit=False)
                     marca.autor = self.request.user
                     marca.save()  
                     data['success'] = 'Marca agregada correctamente'
                 else:
                    data['error'] = form.errors
            else: 
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data)

@method_decorator(staff_member_required, name='dispatch')
class MarcaUpdateView(UpdateView):
    model = Marca
    template_name = "marca/crear.html"
    form_class = MarcaForm
    success_url = reverse_lazy('productos:listarMarcas')  


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Verifica si la acción es 'edit'
            action = request.POST.get('action')
            if action == 'edit':
                form = MarcaForm(request.POST, request.FILES, instance=self.object)
                if form.is_valid():
                    marca = form.save(commit=False)
                    marca.autor = self.request.user  
                    marca.save()  
                    data['success'] = 'Marca actualizado correctamente'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as error:
            data['error'] = str(error)
        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Marca'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        context['entity'] = 'Marca'
        return context

@method_decorator(staff_member_required, name='dispatch') 
class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = "marca/delete.html"
    success_url = reverse_lazy('productos:listarMarcas')  
       
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
        context['title'] = 'Eliminar Marca'
        context['list_url'] = self.success_url
        context['entity'] = 'Marca'
        return context