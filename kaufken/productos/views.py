from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from productos.forms import ProductoForm, CategoriaForm, MarcaForm
from django.contrib.admin.views.decorators import staff_member_required
from productos.models import Producto, Marca, Categoria
import json
from django.views.decorators.http import require_POST


# Create your views here.
@staff_member_required
def manejoInventario(request):
    return render(request, 'base_modal.html')

@staff_member_required
def crearProductos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) 
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
        
    return render(request, 'form_productos.html', {"form": form})

def listarProductos(request):
    productos = Producto.objects.all().order_by('updated_at')
    paginator = Paginator(productos, 4)  # 3 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"Total de productos: {productos.count()}, Total de páginas: {paginator.num_pages}")

    return render(request, 'producto_lista.html', {'page_obj': page_obj})

def buscarProducto(request):
    keyword = request.POST.get("keyword")
    productos = Producto.objects.filter(
        Q(nombre__icontains=keyword) | Q(codigo_qr__icontains=keyword)
        ).order_by('updated_at')
    return render(request, 'producto_lista.html', {'productos': productos})

def editarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Manejo de errores
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)  # Maneja archivos si es necesario
        if form.is_valid():
            form.save()
            # Respuesta para htmx
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "productListChanged": None,
                        "showMessage": f"{producto.nombre} Actualizado."  # Mensaje de éxito
                    })
                }
            )
    else:
        form = ProductoForm(instance=producto)
    
    # Renderiza la plantilla para la edición del producto
    return render(request, 'form_productos.html', {'form': form, 'producto': producto})


@ require_POST
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "productListChanged": None,
                "showMessage": f"{producto.nombre} Eliminado."
            })
        })