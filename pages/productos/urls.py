from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('crear/', views.crearProductos, name="crear"),
    path('listar/', views.listarProductos, name="listarProductos"),
    path('editarProducto/<int:codigo_qr>/', views.editarProducto, name="editarProducto"),
    path('eliminarProducto/<int:codigo_qr>/', views.eliminar_producto, name="eliminarProducto"),
    path('inventario/', views.manejoInventario, name="manejoInventario"),
    path('buscarProducto/', views.buscarProducto, name="buscarProducto"),
]
