from django.urls import path
from app.productos.views.producto import views

app_name = 'productos'

urlpatterns = [
    
    # Producto URLs
    path('crear/', views.crearProductos, name="crear"),
    path('Inventario/', views.ProductoListView.as_view(), name="listarProductos"),
]
