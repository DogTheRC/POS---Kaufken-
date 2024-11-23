from django.urls import path
from app.productos.views.producto import views
from app.productos.views.categoria import views as views_categoria
from app.productos.views.marca import views as views_marca

app_name = 'productos'

urlpatterns = [
    
    # Producto URLs
    path('crear/', views.ProductoCreateView.as_view(), name="crearProductos"),
    path('inventario/', views.ProductoListView.as_view(), name="listarProductos"),
    path('editar/<str:codigo_barra>/', views.ProductoUpdateView.as_view(), name="editarProductos"),
    path('delete/<str:codigo_barra>/', views.ProductoDeleteView.as_view(), name="eliminarProductos"),
    
    #Categorias URLs
    path('categorias/', views_categoria.CategoriaListView.as_view(), name="listarCategorias"),
    path('categorias/crear/', views_categoria.CategoriaCreateView.as_view(), name="crearCategorias"),
    path('categorias/editar/<int:pk>/', views_categoria.CategoriaUpdateView.as_view(), name="editarCategorias"),
    path('categorias/delete/<int:pk>/', views_categoria.CategoriaDeleteView.as_view(), name="eliminarCategorias"),
    #Marcas URLs
    path('marcas/', views_marca.MarcaListView.as_view(), name="listarMarcas"),
    path('marcas/crear/', views_marca.MarcaCreateView.as_view(), name="crearMarcas"),
    path('marcas/editar/<int:pk>/', views_marca.MarcaUpdateView.as_view(), name="editarMarcas"),
    path('marcas/delete/<int:pk>/', views_marca.MarcaDeleteView.as_view(), name="eliminarMarcas"),
    

]
