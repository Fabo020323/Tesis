from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from base.modules.configuracion.models import Configuracion
from base.modules.contenedor.models import Contenedor
from base.modules.historial_sms.models import HistorialSms
from base.modules.orden.models import Orden
from base.modules.pallet.models import Pallet
from base.modules.paquete.models import Paquete
from paqueteria.utils import filter_query_date_range, update_paginate


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


class ConfigurationOrdenListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Orden
    template_name = 'configuracion/configuracion_orden.html'
    success_url = reverse_lazy('conforden')
    permission_required = 'base.configuraciones_superusuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Orden', 'url': reverse_lazy('conforden')},
        ]
        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                orden = request.POST.get('id_orden', '')
                orden = get_object_or_404(Orden, id_orden=orden)
                sigla_estado = request.POST.get('sigla_estado', '')
                orden.cambiar_estado_directo(request.user, sigla_estado)
                messages.success(request, f'Actualizado orden #{orden} con estado {sigla_estado}')
        except:
            messages.error(request, 'No se pudo cambiar los valores')
        return redirect('conforden')


class ConfigurationPaqueteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Paquete
    template_name = 'configuracion/configuracion_paquete.html'
    success_url = reverse_lazy('confpaquete')
    permission_required = 'base.configuraciones_superusuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Paquete', 'url': reverse_lazy('confpaquete')},
        ]
        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                paquete = request.POST.get('id_paquete', '')
                hbl_llenar_orden, bulto = paquete.split('-')
                paquete = get_object_or_404(Paquete, hbl_llenar_orden=hbl_llenar_orden, bulto=int(bulto))
                paquete = Paquete.objects.get(pk=paquete.pk)
                sigla_estado = request.POST.get('sigla_estado', '')
                paquete.change_state_direct(request.user, sigla_estado)
                messages.success(request, f'Actualizado paquete #{paquete} con estado {sigla_estado}')
        except:
            messages.error(request, 'No se pudo cambiar los valores')
        return redirect('confpaquete')


class ConfigurationPalletListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pallet
    template_name = 'configuracion/configuracion_pallet.html'
    success_url = reverse_lazy('confpallet')
    permission_required = 'base.configuraciones_superusuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Pallet', 'url': reverse_lazy('confpallet')},
        ]
        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                pallet = request.POST.get('id_pallet', '')
                pallet = Pallet.objects.get(identificacion_interna=pallet)
                sigla_estado = request.POST.get('sigla_estado', '')
                pallet.cambio_estado_directo(request.user, sigla_estado)
                messages.success(request, f'Actualizado pallet #{pallet} con estado {sigla_estado}')
        except:
            messages.error(request, 'No se pudo cambiar los valores')
        return redirect('confpallet')


class ConfigurationContenedorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Contenedor
    template_name = 'configuracion/configuracion_contenedor.html'
    success_url = reverse_lazy('confcontenedor')
    permission_required = 'base.configuraciones_superusuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Contenedor', 'url': reverse_lazy('confcontenedor')},
        ]
        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                contenedor = request.POST.get('id_contenedor', '')
                contenedor = Contenedor.objects.get(identificacion_interna=contenedor)
                sigla_estado = request.POST.get('sigla_estado', '')
                contenedor.cambio_estado_directo(request.user, sigla_estado)
                messages.success(request, f'Actualizado pallet #{contenedor} con estado {sigla_estado}')
        except:
            messages.error(request, 'No se pudo cambiar los valores')
        return redirect('confpallet')


# Historial de Sms que no se enviaron
class ConfiguracionHistorialSMSListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = HistorialSms
    template_name = 'configuracion/configuracion_sms.html'
    paginate_by = update_paginate()
    permission_required = 'base.list_historial_sms'

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('i', update_paginate())
        return int(paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        date_range = self.request.GET.get("r")
        if query:
            queryset = (queryset.filter(telefono__icontains=query) |
                        queryset.filter(cliente__nombre_primero__icontains=query) |
                        queryset.filter(cliente__nombre_segundo__icontains=query) |
                        queryset.filter(cliente__apellido_primero__icontains=query) |
                        queryset.filter(cliente__apellido_segundo__icontains=query) |
                        queryset.filter(cliente__telefono__icontains=query) |
                        queryset.filter(cliente__licencia__icontains=query) |
                        queryset.filter(cliente__identidad__icontains=query) |
                        queryset.filter(cliente__pasaporte__icontains=query) |
                        queryset.filter(mensaje__icontains=query) |
                        queryset.filter(orden__id_orden__icontains=query))
        queryset = queryset.filter(estado=False)
        return filter_query_date_range(date_range, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['r'] = self.request.GET.get("r", "")
        context['i'] = self.request.GET.get('i', update_paginate())
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Historial de SMS Rechazadas', 'url': reverse_lazy('confsms')},
        ]
        return context
