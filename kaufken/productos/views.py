from django.shortcuts import render, redirect
from productos.forms import ProductoForm, CategoriaForm, MarcaForm
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def crearProductos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para las imágenes
        if form.is_valid():
            producto = form.save( commit = False )
            producto.autor = request.user
            producto.save()
            return redirect("/")  # Redirige a la página principal o a donde desees
    else:
        form = ProductoForm()
        
    return render(request, 'crearProductos.html', {"form": form})