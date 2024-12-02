from django.urls import path
from app.ventas.views.venta import views
from app.ventas.views.detalle_venta import views as views_detalle

app_name = 'ventas'

urlpatterns = [
    # Notificacion URLs
    path('venta/', views.VentaView.as_view(), name="crearVentas"),
    path('registro/', views.VentaListView.as_view(), name="listarVentas"),
    path('registro/delete/<int:pk>/', views.VentaDeleteView.as_view(), name="eliminarVentas"),
    
    # Detalle Ventas
    path('detalle/', views_detalle.DetalleListView.as_view(), name="listarDetalles"),
]
