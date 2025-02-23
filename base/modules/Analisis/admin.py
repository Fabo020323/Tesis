from django.contrib import admin
from base.modules.Analisis.models import Analisis


class AnalisisAdmin(admin.ModelAdmin):
    fields = ['imagen','texto_extraido', 'tipo']


admin.site.register(Analisis, AnalisisAdmin)
