from django.db import models
from base.modules.Imagen.models import Imagen


class Analisis(models.Model):
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='analisis')
    texto_extraido = models.TextField(max_length=1000, default='')
    tipo = models.TextField(max_length=20, default='')

    class Meta:
        verbose_name = 'Analisis'
        verbose_name_plural = 'Analisis'

    def __str__(self):
        return f'{self.imagen.nombre}: {self.texto_extraido}'
