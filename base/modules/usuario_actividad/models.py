from django.db import models
from base.modules.usuario.models import CustomUser


class UsuarioActividad(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()
