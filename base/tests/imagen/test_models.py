from datetime import timedelta

from django.test import TestCase
from base.modules.Imagen.models import Imagen


#Cobertura de Sentencias
from django.test import TestCase
from django.utils.timezone import now
from base.modules.Grupos_Imagenes.models import Grupo
from base.modules.usuario.models import CustomUser


class ImagenTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="testuser@example.com")
        self.grupo = Grupo.objects.create(nombre="Grupo de Prueba")
        self.imagen = Imagen.objects.create(
            nombre="Imagen de Prueba",
            user=self.user,
            grupo=self.grupo
        )

    def test_run_analizado(self):
        self.assertFalse(self.imagen.analizado)
        self.assertIsNone(self.imagen.fecha_analizado)
        self.imagen.run_analizado()
        self.assertTrue(self.imagen.analizado)
        self.assertIsNotNone(self.imagen.fecha_analizado)
        self.assertAlmostEqual(self.imagen.fecha_analizado, now(),delta=timedelta(seconds=2))

    def test_defaults(self):
        self.assertFalse(self.imagen.analizado)
        self.assertEqual(self.imagen.descripcion, "")
        self.assertIsNone(self.imagen.fecha_analizado)
        self.assertIsNotNone(self.imagen.fecha_creacion)

    def test_str_representation(self):
        self.assertEqual(str(self.imagen), "Imagen de Prueba")

    def test_hay_texto_extraido_false(self):
        self.assertFalse(self.imagen.hay_texto_extraido)

    def test_hay_texto_extraido_true(self):
        from base.modules.Analisis.models import Analisis
        analisis = Analisis.objects.create(imagen=self.imagen, texto_extraido="Texto de prueba")
        self.assertTrue(self.imagen.hay_texto_extraido)

    def test_obtener_texto_extraido_falla(self):
        texto = self.imagen.obtener_texto_extraido()
        self.assertEqual(texto, "El Analisis tuvo una falla")

    def test_obtener_texto_extraido_exitoso(self):
        from base.modules.Analisis.models import Analisis
        analisis = Analisis.objects.create(imagen=self.imagen, texto_extraido="Texto extraído")
        texto = self.imagen.obtener_texto_extraido()
        self.assertEqual(texto, "Texto extraído")