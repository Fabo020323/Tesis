import os
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from base.modules.Analisis.models import Analisis
from base.modules.Grupos_Imagenes.models import Grupo
from base.modules.Imagen.forms import ImagenForm
from base.modules.Imagen.models import Imagen
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView, TemplateView
from base_Fabian import settings
from base_Fabian.utils import update_paginate, filter_query_date_range
from django.urls import reverse_lazy


class ImagenListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Imagen
    template_name = 'imagen/lista_de_imagenes.html'
    permission_required = 'base.lista_de_imagen'
    paginate_by = update_paginate()

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('i', update_paginate())
        return int(paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', "")
        context['r'] = self.request.GET.get('r', "")
        context['i'] = self.request.GET.get('i', update_paginate())
        context['breadcrumbs'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Imágenes', 'url': reverse_lazy('lista_de_imagen')},
        ]
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Imagen.objects.filter(user=user)
        query = self.request.GET.get('q', "")
        date_range = self.request.GET.get("r", "")
        if query:
            queryset = (queryset.filter(nombre__icontains=query))
        return filter_query_date_range(date_range, queryset, 'fecha')


class ImagenCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Imagen
    form_class = ImagenForm
    template_name = 'imagen/crear_imagen.html'
    success_url = reverse_lazy('lista_de_imagen')
    permission_required = 'base.add_imagen'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save()
            imagen.user = request.user
            imagen.save()
            messages.success(request, 'Imagen registrado correctamente!')
        else:
            for field, errors in form.errors.items():
                msg = f"{field}: " + "\n".join(errors)
                messages.error(request, msg)
        return redirect('lista_de_imagen')


class ImagenUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Imagen
    template_name = 'imagen/actualizar_imagen.html'
    form_class = ImagenForm
    success_url = reverse_lazy('lista_de_imagen')
    permission_required = 'base.change_imagen'


class ImagenDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Imagen
    template_name = 'imagen/eliminar_imagen.html'
    permission_required = 'base.delete_imagen'


class ExtraerTextoViewPlano(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'base.extract_plano'
    success_url = reverse_lazy('lista_de_imagen')

    def get(self, request, *args, **kwargs):
        from base.modules.modelo_IA.modelo_ia import model, tokenizer
        imagen_id = kwargs.get('pk')
        imagen = get_object_or_404(Imagen, id=imagen_id)

        referer_url = request.META.get('HTTP_REFERER', self.success_url)

        if imagen.analizado is True:
            messages.error(request, 'La imagen ya ha sido analizada')
            return redirect(referer_url)

        if not imagen.imagen:
            messages.error(request, "NO existe imagen asociada a esta instancia")
            return redirect(referer_url)

        # path_image_temp = imagen.imagen.url
        path_image_temp = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
        try:
            res = model.chat(tokenizer, path_image_temp, ocr_type='ocr')

            extraccion = Analisis.objects.create(
                imagen=imagen,
                texto_extraido=res
            )
            imagen.run_analizado()
            messages.success(request, "El texto ha sido extraído correctamente")
        except Exception as e:
            messages.error(request, "Ha ocurrido un error durante el proceso" + str(e))
        return redirect(referer_url)


class VerAnalisisPlanoView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'base.view_analisis_imagen'
    template_name = 'imagen/ver_analisis_plano.html'
    model = Imagen
    success_url = reverse_lazy('lista_de_imagen')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imagen = get_object_or_404(Imagen, pk=self.kwargs['pk'])
        context['analisis'] = imagen.obtener_texto_extraido()
        return context


class ExtraerTextoViewFormateado(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'base.extract_formateado'
    success_url = reverse_lazy('lista_de_imagen')

    def get(self, request, *args, **kwargs):
        from base.modules.modelo_IA.modelo_ia import model, tokenizer
        imagen_id = kwargs.get('pk')
        imagen = get_object_or_404(Imagen, id=imagen_id)

        referer_url = request.META.get('HTTP_REFERER', self.success_url)

        if imagen.analizado is True:
            messages.error(request, 'La imagen ya ha sido analizada')
            return redirect(referer_url)

        if not imagen.imagen:
            messages.error(request, "NO existe imagen asociada a esta instancia")
            return redirect(referer_url)

        # path_image_temp = imagen.imagen.url
        path_image_temp = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
        try:
            res = model.chat(tokenizer, path_image_temp, ocr_type='format')

            extraccion = Analisis.objects.create(
                imagen=imagen,
                texto_extraido=res
            )
            imagen.run_analizado()
            messages.success(request, "El texto ha sido extraído correctamente")
        except Exception as e:
            messages.error(request, "Ha ocurrido un error durante el proceso" + str(e))
        return redirect(referer_url)


class VerAnalisisFormateadoView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'base.view_analisis_imagen_formateado'
    template_name = 'imagen/ver_analisis_formateado.html'
    model = Imagen
    success_url = reverse_lazy('lista_de_imagen')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imagen = get_object_or_404(Imagen, pk=self.kwargs['pk'])
        context['analisis'] = imagen.obtener_texto_extraido()
        return context