from django.db import models
from django.utils.timezone import now

from base.modules.Grupos_Imagenes.models import Grupo
from base.modules.usuario.models import CustomUser


class Imagen(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True, default='default/OCR.png')
    descripcion = models.TextField(max_length=100, null=True, blank=True, default='')
    analizado = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='user_imagen')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_analizado = models.DateTimeField(null=True, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True, related_name='imagenes')

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'
        ordering = ['analizado','fecha_creacion']
        permissions = [('lista_de_imagen', 'Lista de Imagenes'),
                       ('extract_plano', 'Extraer en texto plano'),
                       ('view_analisis_imagen', 'Puede ver análisis de imágenes'),
                       ('view_imagenes_grupo','Ver Imágenes de un Grupo'),
                       ('extract_formateado','Extraer Texto Formateado'),
                       ]

    def __str__(self):
        return self.nombre

    def run_analizado(self):
        self.analizado = True
        self.fecha_analizado = now()
        self.save()

    @property
    def hay_texto_extraido(self):
        return self.analisis.exists()

    def obtener_texto_extraido(self):
        analisis = self.analisis.first()
        if analisis:
            return analisis.texto_extraido
        return 'El Analisis tuvo una falla'
