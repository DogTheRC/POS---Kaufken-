from django.urls import path
from app.productos.views.producto import views

app_name = 'productos'

urlpatterns = [
    
    # Producto URLs
    path('crear/', views.ProductoCreateView.as_view(), name="crearProductos"),
    path('inventario/', views.ProductoListView.as_view(), name="listarProductos"),
    path('editar/<str:codigo_qr>/', views.ProductoUpdateView.as_view(), name="editarProductos"),
    path('delete/<str:codigo_qr>/', views.ProductoDeleteView.as_view(), name="eliminarProductos"),
]
