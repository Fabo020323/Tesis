from django.contrib import admin
from base.modules.Imagen.models import Imagen


class ImagenAdmin(admin.ModelAdmin):
    fields = ['nombre', 'imagen', 'descripcion', 'analizado', 'fecha_creacion', 'fecha_analizado']


admin.site.register(Imagen, ImagenAdmin)
