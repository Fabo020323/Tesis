from django.db import models


class Tipo(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
