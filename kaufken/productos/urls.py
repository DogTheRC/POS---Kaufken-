from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('crear/', views.crearProductos, name="crear"),
    path('tablaProductos/', views.listarProductos, name="listarProductos"),
    path('editarProducto/<int:id>/', views.editarProducto, name="editarProducto"),
]
