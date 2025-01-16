from django.utils import timezone

from base.modules.usuario_actividad.models import UsuarioActividad


class UsuarioActividadMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            UsuarioActividad.objects.update_or_create(
                user=request.user,
                defaults={'last_activity': timezone.now()}
            )

        response = self.get_response(request)

        return response
