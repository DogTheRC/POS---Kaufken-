from typing import Any
from app.notificaciones.models import Notificacion
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class NotificacionesListView(ListView):
    model = Notificacion
    template_name = "notificacion_stock.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        # Mostrar solo notificaciones del usuario autenticado y ordenadas por la fecha de creación (más recientes primero)
        return Notificacion.objects.filter(usuario=self.request.user, leido=False).order_by('-created_at')
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Notificacion.objects.all().order_by('-created_at').filter(leido=False):
                    data.append(i.toJSON())
            elif action == 'mark_as_read':
                # Obtener el ID de la notificación y marcarla como leída
                notificacion_id = request.POST.get('id')
                notificacion = Notificacion.objects.get(id=notificacion_id)
                notificacion.leido = True
                notificacion.save()
                data = {'success': 'Notificación marcada como leída'}
            else:
                data['error'] = 'No a ingresado ninguna accion'
        except Exception as error:
            data = {'error': str(error)}
        return JsonResponse(data, safe=False)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_notifications'] = Notificacion.objects.filter(usuario=self.request.user, leido=False).exists()
        context['title'] = 'Notificaciones'
        context['entity'] = 'Producto'
        return context
    
