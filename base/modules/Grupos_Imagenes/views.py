import os
from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from base.modules.Analisis.models import Analisis
from base.modules.Grupos_Imagenes.forms import GrupoForm
from base.modules.Grupos_Imagenes.models import Grupo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView

from base.modules.Imagen.models import Imagen
from base.modules.Tipo.models import Tipo
from base_Fabian import settings
from base_Fabian.utils import update_paginate, filter_query_date_range
from django.urls import reverse_lazy
from PIL import Image as PilImage


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
        context['t'] = self.request.GET.get('t', "")
        context['i'] = self.request.GET.get('i', update_paginate())
        context['grupos'] = Grupo.objects.all()
        context['breadcrumbs'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Grupos', 'url': reverse_lazy('lista_de_grupo')},
        ]
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Grupo.objects.filter(user=user)
        query = self.request.GET.get('q', "")
        grupo = self.request.GET.get('t', "")
        if grupo:
            queryset = queryset.filter(grupo=grupo)
        date_range = self.request.GET.get("r", "")
        if query:
            queryset = (queryset.filter(nombre__icontains=query))
        return filter_query_date_range(date_range, queryset, 'fecha_creacion')


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
                if not imagen.sin_formato:
                    path_image_temp = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
                    try:
                        res = model.chat(tokenizer, path_image_temp, ocr_type='ocr')
                        extraccion = Analisis.objects.create(
                            imagen=imagen,
                            texto_extraido=res,
                            tipo=Tipo.objects.get(pk=1)
                        )
                        imagen.run_sin_formato()
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


class ReporteImagenesPDFView(View):
    def draw_wrapped_text(self, p, text, x, y, max_width, font_name="Helvetica", font_size=10, leading=12):
        lines = simpleSplit(text, font_name, font_size, max_width)
        for line in lines:
            p.drawString(x, y, line)
            y -= leading
        return y

    def get(self, request, grupo_id, *args, **kwargs):
        grupo = Grupo.objects.get(pk=grupo_id)
        tipo_analisis_textual = Tipo.objects.get(pk=1)  # Ajusta según tu lógica

        imagenes = Imagen.objects.filter(grupo=grupo, analisis__tipo=tipo_analisis_textual).distinct()

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        y = height - 50
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"Reporte de imágenes del grupo: {grupo.nombre}")
        y -= 40

        for imagen in imagenes:
            if y < 150:
                p.showPage()
                y = height - 50

            # Imagen
            if imagen.imagen:
                try:
                    img_path = imagen.imagen.path
                    pil_img = PilImage.open(img_path)
                    aspect = pil_img.width / pil_img.height
                    img_width = 150
                    img_height = img_width / aspect

                    p.drawInlineImage(img_path, 50, y - img_height, width=img_width, height=img_height)
                except Exception:
                    p.drawString(50, y, "(Error al cargar imagen)")
                    img_height = 0
            else:
                img_height = 0

            # Texto al lado de la imagen
            x_text = 220
            y_text = y

            p.setFont("Helvetica-Bold", 12)
            p.drawString(x_text, y_text, f"Nombre: {imagen.nombre}")
            y_text -= 15

            p.setFont("Helvetica", 10)
            y_text = self.draw_wrapped_text(p, f"Descripción: {imagen.descripcion}", x_text, y_text,
                                            max_width=width - x_text - 40)
            y_text -= 10

            analisis = imagen.analisis.filter(tipo=tipo_analisis_textual).first()
            texto_extraido = analisis.texto_extraido if analisis else "(No hay análisis textual)"

            p.setFont("Helvetica", 10)
            y_text = self.draw_wrapped_text(p, texto_extraido, x_text, y_text, max_width=width - x_text - 40)

            y -= max(img_height, y - y_text) + 40  # Ajuste vertical para evitar solapamiento

        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_grupo_{grupo.nombre}.pdf"'
        response.write(pdf)
        return response