import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.core.mail import send_mail
from base.modules.usuario.models import CustomUser
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from base.modules.usuario.forms import UserForm, ThemeSettingsForm
from django.contrib.auth.models import Group
from django.contrib import messages

from base_Fabian.utils import update_paginate


class UsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'usuario/lista_usuario.html'
    context_object_name = 'usuarios'
    paginate_by = update_paginate()
    permission_required = 'base.list_customuser'

    def has_permission(self):
        return self.request.user.has_perm('base.list_customuser')

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('i', update_paginate())
        return int(paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False).distinct()
        query = self.request.GET.get("q", "")
        if query:
            queryset = (queryset.filter(first_name__icontains=query) |
                        queryset.filter(last_name__icontains=query) |
                        queryset.filter(email__icontains=query) |
                        queryset.filter(groups__name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", "")
        context['i'] = self.request.GET.get('i', update_paginate())
        context['form'] = UserForm
        context['breadcrumb'] = [
            {'text': 'Inicio', 'url': '/'},
            {'text': 'Usuarios', 'url': '/usuarios/'},
        ]
        return context


class UsuarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy('usuarios_listado')
    permission_required = 'base.add_customuser'

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.save()
            usuario.groups.clear()
            grupo = request.POST.get('group')
            grupo = Group.objects.get(id=grupo)
            usuario.groups.add(grupo)

            usuario.save()
            # Enviar correo al usuario
            try:
                subject = "Bienvenido a la plataforma"
                message = f"Hola {usuario.first_name},\n\nTu cuenta ha sido creada exitosamente.\n\nUsuario: {usuario.username}\n Su contraseña es {usuario.password}"
                email_from = 'fabiantesis23@gmail.com'
                recipient_list = [usuario.email]

                send_mail(subject, message, email_from, recipient_list)

                messages.success(request, 'Usuario registrado correctamente y correo enviado!')
            except Exception as e:
                messages.error(request, f"Usuario registrado, pero ocurrió un error al enviar el correo: {str(e)}")
        else:
            for field, errors in form.errors.items():
                msg = f"{field}: " + "\n".join(errors)
                messages.error(request, msg)
        return redirect('usuarios_listado')


class UsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy('usuarios_listado')
    permission_required = 'base.change_customuser'

    def has_permission(self):
        return self.request.user.has_perm('base.list_customuser')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        mutable_post = request.POST.copy()

        if self.request.user.has_perm('base.list_customuser'):
             mutable_post['group'] = str(self.object.groups.first().id)

        form = UserForm(mutable_post, request.FILES, instance=self.object)
        if form.is_valid():
            usuario = form.save(commit=False)
            if self.request.user.is_superuser or self.request.user.has_perm(
                    'base.list_customuser'):
                grupo = request.POST.get('group')
                if grupo:
                    try:
                        grupo = Group.objects.get(id=grupo)
                        usuario.groups.clear()
                        usuario.groups.add(grupo)
                    except Group.DoesNotExist:
                        pass

            usuario.save()
            messages.success(request, 'Usuario actualizado correctamente!')
        else:
            for field, errors in form.errors.items():
                msg = f"{field}: " + "\n".join(errors)
                messages.error(request, msg)
        return redirect('usuarios_listado')


class UsuarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'usuario/eliminar_usuario.html'
    success_url = reverse_lazy('usuarios_listado')
    permission_required = 'base.delete_customuser'


class UsuarioConfiguracionView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'usuario/lista_usuario.html'
    form_class = ThemeSettingsForm
    permission_required = 'base.change_customuser'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                data = json.loads(request.body)
                user_settings = request.user
                user_settings.theme_color_scheme = data.get('theme_color_scheme', user_settings.theme_color_scheme)
                user_settings.layout_mode = data.get('layout', {}).get('mode', user_settings.layout_mode)
                user_settings.layout_width = data.get('layout', {}).get('width', user_settings.layout_width)
                user_settings.topbar_color = data.get('topbar', {}).get('color', user_settings.topbar_color)
                user_settings.menu_color = data.get('menu', {}).get('color', user_settings.menu_color)
                user_settings.sidenav_size = data.get('sidenav', {}).get('size', user_settings.sidenav_size)
                user_settings.save()
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class UsuarioListdatosView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = CustomUser
    permission_required = 'base.list_customuser'

    def has_permission(self):
        return self.request.user.has_perm('base.list_customuser')

    def get(self, request, *args, **kwargs):
        try:
            usuario = get_object_or_404(CustomUser, pk=kwargs['pk'])
            data = {
                'id_username': usuario.username,
                'id_first_name': usuario.first_name,
                'id_email': usuario.email,
                'imagen': usuario.imagen.url,
                'id_last_name': usuario.last_name,
                'id_is_active': usuario.is_active,
                'id_group_mostrar': usuario.groups.first().id if usuario.groups.exists() else None,
                'id_telefono': usuario.telefono,
                'status': 'success'
            }
        except Exception as e:
            data = {
                'status': 'error',
                'message': str(e)
            }

        return JsonResponse(data)
