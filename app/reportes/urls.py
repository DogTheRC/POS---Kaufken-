from django.urls import path
from app.reportes.views.venta import views


app_name = 'reportes'

urlpatterns = [
    # Notificacion URLs
    path('venta/', views.reportVentaView.as_view(), name="reporteVenta"),

]