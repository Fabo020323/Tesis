from django.contrib import admin
from base.modules.usuario_actividad.models import UsuarioActividad


class UsuarioActividadAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'last_activity')


admin.site.register(UsuarioActividad, UsuarioActividadAdmin)
