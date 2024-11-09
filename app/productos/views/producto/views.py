import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from app.productos.forms import ProductoForm, CategoriaForm, MarcaForm
from app.productos.models import Producto, Marca, Categoria

# MIGRACION A CLASES
class ProductoListView(ListView):
    model = Producto
    template_name = "producto/inventario.html"
    @method_decorator(csrf_exempt)
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
        data = Producto.objects.get(pk=request.POST['id']).toJSON()
        return JsonResponse(data)

@method_decorator(staff_member_required, name='dispatch')
class ProductoCreateView(CreateView):
    model = Producto
    template_name = "producto/crear.html"
    form_class = ProductoForm
    success_url = reverse_lazy('productos:listarProductos')  # Redirige a la URL que prefieras tras guardar

    def form_valid(self, form):
        producto = form.save(commit=False)
        producto.autor = self.request.user  # Asignamos el usuario actual como autor
        producto.save()
        return super().form_valid(form)  # Redirige al `success_url` después de guardar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Producto'
        return context













@staff_member_required
def manejoInventario(request):
    return render(request, 'inventario.html')

@staff_member_required
def crearProductos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) 
        print(form)
        if form.is_valid():
            producto = form.save( commit = False )
            producto.autor = request.user
            producto.save()
            return HttpResponse(
                status=204, 
                headers={
                    'HX-Trigger': json.dumps({
                        "productListChanged": None,
                        "showMessage": f"{producto.nombre} Agregado."
                    })
                })

    else:
        form = ProductoForm()
        
    return render(request, 'modals/form_productos.html', {"form": form})

def listarProductos(request):
    productos = list(Producto.objects.values())
    data={'productos':productos}
    return JsonResponse(data)


def buscarProducto(request):
    keyword = request.POST.get("keyword")
    productos = Producto.objects.filter(
        Q(nombre__icontains=keyword) | Q(codigo_qr__icontains=keyword)
        ).order_by('updated_at')
    return render(request, 'tabla_productos.html', {'productos': productos})


def editarProducto(request, codigo_qr):
    producto = get_object_or_404(Producto, codigo_qr=codigo_qr)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            # Respuesta para htmx51
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "productListChanged": None,
                        "showMessage": f"{producto.nombre} Actualizado."
                    })
                }
            )
    else:
        form = ProductoForm(instance=producto)

    # Renderiza la plantilla para la edición del producto
    return render(request, 'modals/form_productos.html', {'form': form, 'producto': producto})

def eliminar_producto(request, codigo_qr):
    producto = get_object_or_404(Producto, codigo_qr=codigo_qr)
    producto.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "productListChanged": None,
                "showMessage": f"{producto.nombre} Eliminado."
            })
        })
        
        