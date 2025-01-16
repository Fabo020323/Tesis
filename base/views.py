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
from django.views.generic import TemplateView
from django.contrib import messages


# from paqueteria.utils import mes_en_espannol, get_config_value


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login'


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('base')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


