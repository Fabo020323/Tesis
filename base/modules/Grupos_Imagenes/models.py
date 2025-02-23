from django.db import models

from base.modules.usuario.models import CustomUser


class Grupo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=100, null=True, blank=True, default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='grupo_user')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['fecha_creacion']
        permissions = [('lista_de_grupo','Listado de Grupos'),('extract_grupo_plano','Extraer A Grupo Plano')]

    def __str__(self):
        return self.nombre