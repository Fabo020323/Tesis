from django.contrib import admin
from base.modules.Grupos_Imagenes.models import Grupo


class GrupoAdmin(admin.ModelAdmin):
    fields = ['nombre','descripcion', 'user']


admin.site.register(Grupo, GrupoAdmin)
