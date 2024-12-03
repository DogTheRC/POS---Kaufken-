
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class StaffMemberRequiredMixin(AccessMixin):
    """
    Mixin para restringir el acceso solo a miembros del personal (staff) activos.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return redirect('admin:login')  

class StaffMemberRequiredMixin(AccessMixin):
    """
    Mixin para restringir el acceso solo a miembros del personal (staff) activos.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return redirect('admin:login')  