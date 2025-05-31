from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from base.modules.configuracion.models import Configuracion


class ConfigurationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Configuracion
    template_name = 'configuracion/configuracion.html'
    success_url = reverse_lazy('configuracion')
    permission_required = 'base.configuraciones_administrador'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Configuración', 'url': reverse_lazy('configuracion')},
        ]
        return context

    def post(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.all()
            data = request.POST
            for config in configuracion:
                config_key = config.llave
                if config_key in data:
                    config.valor = data[config_key]
                    config.save()
            messages.success(request, 'Actualizado los valores de configuración')
        except:
            messages.error(request, 'No se pudo cambiar los valores de configuración')
        return redirect('configuracion')










# Historial de Sms que no se enviaron
