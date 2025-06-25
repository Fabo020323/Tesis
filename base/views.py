import re
from datetime import timedelta
from decimal import Decimal
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
        return context




class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if not user.fecha_activacion:
            return reverse_lazy('modal_password')
        return reverse_lazy('base')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')







