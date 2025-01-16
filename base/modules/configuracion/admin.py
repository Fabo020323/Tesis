from django.contrib import admin

from base.modules.configuracion.models import Configuracion


class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ["llave", "valor"]


admin.site.register(Configuracion, ConfiguracionAdmin)
