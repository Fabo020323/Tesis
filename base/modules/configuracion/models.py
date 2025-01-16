from django.db import models


class Configuracion(models.Model):
    llave = models.CharField(max_length=50, unique=True)
    valor = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Configuracion'
        verbose_name_plural = 'Configuraciones'
        ordering = ['llave']
        permissions = [('configuraciones_administrador', 'Lista de configuraciones'),
                       ('configuraciones_superusuario', 'Lista de configuraciones Superusuario')]
