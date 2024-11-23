from django.urls import path
from app.notificaciones import views

app_name = 'notificacion'

urlpatterns = [
    # Notificacion URLs
    path('notificaciones/', views.NotificacionesListView.as_view(), name="listarNotificaciones"),
]
