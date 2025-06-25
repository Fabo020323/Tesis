import json
import re
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages

from base.modules.Grupos_Imagenes.models import Grupo
from base.modules.Imagen.models import Imagen
from base.modules.usuario.forms import CambiarPasswordForm
from base_Fabian.utils import mes_en_espannol


# from paqueteria.utils import mes_en_espannol, get_config_value


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        cantidad_total_imagenes = Imagen.objects.filter(user=self.request.user).count()
        context['cantidad_total_imagenes'] = cantidad_total_imagenes
        cantidad_imagenes_en_grupos = sum( grupo.cantidad_imaganes() for grupo in Grupo.objects.filter(user=self.request.user))
        context['cantidad_imagenes_en_grupos'] = cantidad_imagenes_en_grupos
        context['cantidad_imagenes_independientes'] = cantidad_total_imagenes - cantidad_imagenes_en_grupos
        cantidad_de_imagenes_analizadas = Imagen.objects.filter(user=self.request.user,analizado=True).count()
        context['cantidad_de_imagenes_analizadas'] = cantidad_de_imagenes_analizadas
        context['cantidad_de_imagenes_sin_analizar'] = cantidad_total_imagenes - cantidad_de_imagenes_analizadas
        context['grupos'] = Grupo.objects.all()
        return context




class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'fecha_activacion': user.fecha_activacion is not None
                })
            return JsonResponse({'success': False, 'error': 'Credenciales inválidas'}, status=401)
        else:
            return super().post(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

@csrf_exempt
@login_required
def cambiar_contrasena_api(request):
    try:
        data = json.loads(request.body)
        password = data.get('password')
        if not password:
            return JsonResponse({'success': False, 'error': 'Falta contraseña'}, status=400)

        user = request.user
        user.set_password(password)
        user.fecha_activacion = timezone.now()
        user.save()

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)





