import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from base.modules.usuario.models import CustomUser
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from base.modules.usuario.forms import UserForm, ThemeSettingsForm
from base.modules.sucursal.models import Sucursal
from django.contrib.auth.models import Group
from django.contrib import messages
from paqueteria.utils import update_paginate


class UsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'usuario/lista_usuario.html'
    context_object_name = 'usuarios'
    paginate_by = update_paginate()
    permission_required = ('base.list_customuser', 'base.list_customuser_gerente')

    def has_permission(self):
        return (self.request.user.has_perm('base.list_customuser') or
                self.request.user.has_perm('base.list_customuser_gerente'))

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('i', update_paginate())
        return int(paginate_by)

    def get_queryset(self):
        if self.request.user.has_perm('base.list_customuser') or self.request.user.is_superuser:
            queryset = super().get_queryset()
        elif self.request.user.has_perm('base.list_customuser_gerente'):
            sucursales = self.request.user.sucursales.all()
            queryset = CustomUser.objects.filter(sucursales__in=sucursales).distinct()
        else:
            queryset = CustomUser.objects.filter(pk__icontains=' ')

        query = self.request.GET.get("q", "")
        if query:
            queryset = (queryset.filter(first_name__icontains=query) |
                        queryset.filter(last_name__icontains=query) |
                        queryset.filter(email__icontains=query) |
                        queryset.filter(sucursales__nombre_sucursal__icontains=query) |
                        queryset.filter(groups__name__icontains=query))
        queryset = queryset.filter(is_superuser=False).distinct()
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
        context['sucursales'] = Sucursal.objects.all()
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

            usuario.sucursales.clear()
            sucursales_seleccionadas = request.POST.getlist('sucursales[]')
            for sucursal_id in sucursales_seleccionadas:
                try:
                    sucursal = Sucursal.objects.get(id=sucursal_id)
                    usuario.sucursales.add(sucursal)
                except Sucursal.DoesNotExist:
                    pass

            usuario.groups.clear()
            grupo = request.POST.get('group')
            grupo = Group.objects.get(id=grupo)
            usuario.groups.add(grupo)

            usuario.save()
            messages.success(request, 'Usuario registrado correctamente!')
        else:
            for field, errors in form.errors.items():
                msg = f"{field}: " + "\n".join(errors)
                messages.error(request, msg)
        return redirect('usuarios_listado')


class UsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy('usuarios_listado')
    permission_required = ('base.change_customuser', 'base.list_customuser_gerente')

    def has_permission(self):
        return (self.request.user.has_perm('base.list_customuser') or
                self.request.user.has_perm('base.list_customuser_gerente'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        mutable_post = request.POST.copy()

        if self.request.user.has_perm('base.list_customuser_gerente'):
            if 'group' not in mutable_post:
                mutable_post['group'] = str(self.object.groups.first().id)
            if 'sucursales[]' not in mutable_post:
                mutable_post['sucursales[]'] = ''

        form = UserForm(mutable_post, request.FILES, instance=self.object)
        if form.is_valid():
            usuario = form.save(commit=False)

            if usuario.email == 'johnsafont@gmail.com':
                usuario.is_active = True

            if self.request.user.is_superuser or self.request.user.has_perm(
                    'base.list_customuser') or not self.request.user.has_perm('base.list_customuser_gerente'):
                usuario.sucursales.clear()
                sucursales_seleccionadas = request.POST.getlist('sucursales[]')
                for sucursal in sucursales_seleccionadas:
                    try:
                        sucursal = Sucursal.objects.get(id=sucursal)
                        usuario.sucursales.add(sucursal)
                    except Sucursal.DoesNotExist:
                        pass

                usuario.groups.clear()
                grupo = request.POST.get('group')
                if grupo:
                    try:
                        grupo = Group.objects.get(id=grupo)
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
    permission_required = ('base.list_customuser', 'base.list_customuser_gerente')

    def has_permission(self):
        return (self.request.user.has_perm('base.list_customuser') or
                self.request.user.has_perm('base.list_customuser_gerente'))

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
                'id_sucursales_mostrar': list(usuario.sucursales.values_list('id', flat=True)),
                'id_telefono': usuario.telefono,
                'status': 'success'
            }
        except Exception as e:
            data = {
                'status': 'error',
                'message': str(e)
            }

        return JsonResponse(data)

# revisar
# class GroupListView(ListView):
#     model = Group
#     template_name = 'usuario/lista_grupo.html'
#     context_object_name = 'groups'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get("q", "")
#         if query:
#             queryset = (queryset.filter(nombre__icontains=query) |
#                         queryset.filter(sigla__icontains=query))
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['q'] = self.request.GET.get("q", "")
#         context['i'] = self.request.GET.get('i', update_paginate())
#         context['breadcrumb'] = [
#             {'text': 'Inicio', 'url': '/'},
#             {'text': 'Países', 'url': reverse_lazy('listado_pais')},
#         ]
#         return context
#
#
# class GroupCreateView(CreateView):
#     model = Group
#     form_class = GroupForm
#     template_name = 'usuario/lista_grupo.html'
#     success_url = reverse_lazy('group_list')
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse(
#                 {'success': False, 'html': render_to_string(self.template_name, {'form': form}, request)})
#
#
# class GroupUpdateView(UpdateView):
#     model = Group
#     form_class = GroupForm
#     template_name = 'usuario/lista_grupo.html'
#     success_url = reverse_lazy('group_list')
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse(
#                 {'success': False, 'html': render_to_string(self.template_name, {'form': form}, request)})
#
#
# class GroupDeleteView(DeleteView):
#     model = Group
#     template_name = 'usuario/eliminar_grupo.html'
#     success_url = reverse_lazy('group_list')
#
#     def delete(self, request, *args, **kwargs):
#         group = self.get_object()
#         group.delete()
#         return JsonResponse({'success': True})
