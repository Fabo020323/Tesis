import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from base.modules.Analisis.models import Analisis
from base.modules.Grupos_Imagenes.forms import GrupoForm
from base.modules.Grupos_Imagenes.models import Grupo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView

from base.modules.Imagen.models import Imagen
from base_Fabian import settings
from base_Fabian.utils import update_paginate, filter_query_date_range
from django.urls import reverse_lazy


class GrupoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Grupo
    template_name = 'grupo/lista_de_grupos.html'
    permission_required = 'base.lista_de_grupo'
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
            {'text': 'Grupos', 'url': reverse_lazy('lista_de_grupo')},
        ]
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Grupo.objects.filter(user=user)
        query = self.request.GET.get('q', "")
        date_range = self.request.GET.get("r", "")
        if query:
            queryset = (queryset.filter(nombre__icontains=query))
        return filter_query_date_range(date_range, queryset, 'fecha')


class GrupoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'grupo/crear_grupo.html'
    success_url = reverse_lazy('lista_de_grupo')
    permission_required = 'base.add_grupo'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save()
            imagen.user = request.user
            imagen.save()
            messages.success(request, 'Grupo registrado correctamente!')
        else:
            for field, errors in form.errors.items():
                msg = f"{field}: " + "\n".join(errors)
                messages.error(request, msg)
        return redirect('lista_de_grupo')


class GrupoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Grupo
    template_name = 'grupo/actualizar_grupo.html'
    form_class = GrupoForm
    success_url = reverse_lazy('lista_de_grupo')
    permission_required = 'envios.change_grupo'


class GrupoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Grupo
    template_name = 'grupo/eliminar_grupo.html'
    success_url = reverse_lazy('lista_de_grupo')
    permission_required = 'envios.delete_grupo'


class ExtraerTextoGrupoPlanoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'extract_grupo_plano'

    def get(self, request, *args, **kwargs):
        from base.modules.modelo_IA.modelo_ia import model, tokenizer
        grupo_id = kwargs.get('pk')
        grupo = get_object_or_404(Grupo, id=grupo_id)

        imagenes = grupo.imagenes.all()

        if not imagenes:
            messages.error(request, 'No hay imágenes asociadas a este grupo.')
            return redirect('lista_de_grupo')

        for imagen in imagenes:
            if imagen.imagen:
                if not imagen.analizado:
                    path_image_temp = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
                    try:
                        res = model.chat(tokenizer, path_image_temp, ocr_type='ocr')

                        extraccion = Analisis.objects.create(
                            imagen=imagen,
                            texto_extraido=res,
                            tipo='plano'
                        )

                        imagen.run_analizado()
                        messages.success(request, "El texto ha sido extraído correctamente")

                    except Exception as e:
                        messages.error(request, f"No se ha podido procesar la imagen {imagen.nombre}")
        return redirect('lista_de_grupo')


class ListImagenesGruposView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'base.view_grupo'
    template_name = 'grupo/lista_de_imagen.html'

    def get_queryset(self):
        queryset = Imagen.objects.all()
        query = self.request.GET.get('q', '')
        if query:
            queryset = (queryset.filter(nombre__icontains=query) |
                        queryset.filter(descripcion__icontains=query))
        return queryset

    def get_paginater_by(self, queryset):
        paginate_by = self.request.GET.get('i', update_paginate())
        return int(paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            grupo = Grupo.objects.filter(pk=self.kwargs['pk'])
            imagenes = Imagen.objects.filter(grupo__pk=self.kwargs['pk'])
            paginator = Paginator(imagenes, self.get_paginater_by(imagenes))

            page_number = self.request.GET.get('page')
            imagenes_page = paginator.get_page(page_number)

            context['imagenes'] = imagenes
            context['grupo'] = grupo

            context['page_obj'] = imagenes_page
            context['is_paginated'] = imagenes_page.has_other_pages()
            context['q'] = self.request.GET.get('q', '')
            context['i'] = self.request.GET.get('i', update_paginate())
            context['breadcrumb'] = [
                {'text': 'Inicio', 'url': '/'},
                {'text': 'Grupos', 'url': reverse_lazy('lista_de_grupo')}

            ]
        except Exception as e:
            messages.error(self.request, 'Ha ocurrido un error en la solicitud')
        return context
