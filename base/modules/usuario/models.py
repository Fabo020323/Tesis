from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    theme_color_scheme = models.CharField(max_length=10, default='light')
    layout_mode = models.CharField(max_length=10, default='default')
    layout_width = models.CharField(max_length=10, default='default')
    topbar_color = models.CharField(max_length=10, default='light')
    menu_color = models.CharField(max_length=10, default='light')
    menu_icon = models.CharField(max_length=10, default='default')
    sidenav_size = models.CharField(max_length=10, default='default')
    sidebar_user_info = models.BooleanField(default=False)
    sidenav_twocolumn = models.CharField(max_length=10, default='light')
    imagen = models.ImageField(upload_to='imagen_usuario/', blank=True, null=True, default='default/spiderman.png')
    telefono = models.CharField(max_length=10, default='', blank=True, null=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']
        permissions = [('list_customuser', 'Lista de Usuarios'), ('permiso_sms', 'Permisos SMS'),
                       ('list_customuser_gerente', 'Lista de Usuarios Gerente')]

    def __str__(self):
        return self.username

    @property
    def get_full_names(self):
        return super().get_full_name()

    @property
    def get_rules(self):
        groups = self.groups.all()
        if groups:
            return ", ".join(group.name for group in groups)
        else:
            return "Sin grupo"

    @property
    def get_principal_sucursal(self):
        primary_sucursales = self.sucursales.filter(primaria=True)
        if primary_sucursales.exists():
            return primary_sucursales.first()
        elif self.sucursales.exists():
            return self.sucursales.first()
        else:
            return None

    @property
    def get_active_users(self):
        from base.modules.usuario_actividad.models import UsuarioActividad
        time_threshold = timezone.now() - timedelta(minutes=5)
        if UsuarioActividad.objects.filter(last_activity__gte=time_threshold, user=self):
            return True
        return False
