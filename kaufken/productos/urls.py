from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('crear/', views.crearProductos, name="crear"),
    path('listar/', views.listarProductos, name="listarProductos"),
    path('editarProducto/<int:id>/', views.editarProducto, name="editarProducto"),
    path('eliminarProducto/<int:id>/', views.eliminar_producto, name="eliminarProducto"),
    path('inventario/', views.manejoInventario, name="manejoInventario"),
    path('buscarProducto/', views.buscarProducto, name="buscarProducto"),
]
