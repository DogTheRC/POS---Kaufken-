from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from pages.productos.forms import ProductoForm, CategoriaForm, MarcaForm
from django.contrib.admin.views.decorators import staff_member_required
from pages.productos.models import Producto, Marca, Categoria
import json
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http.response import JsonResponse
# Create your views here.

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
    productos = Producto.objects.all().order_by('updated_at')
    paginator = Paginator(productos, 4)  # 3 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(44, productos)
    print(f"Total de productos: {productos.count()}, Total de páginas: {paginator.num_pages}")
    return render(request, 'tabla_productos.html', {'productos': page_obj})

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
        