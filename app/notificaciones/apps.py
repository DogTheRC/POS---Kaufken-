from django.apps import AppConfig


class NotificacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.notificaciones'
    
    def ready(self):
        import app.notificaciones.signals
