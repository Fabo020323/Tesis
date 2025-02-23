from django.urls import path
from base.modules.usuario.views import *

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuarios_listado'),
    path('crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('actualizar/<int:pk>/', UsuarioUpdateView.as_view(), name='actualizar_usuario'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('configuracion_usuario/', UsuarioConfiguracionView.as_view(), name='configuracion_usuario'),
    path('<int:pk>/datos/', UsuarioListdatosView.as_view(), name='usuario_datos'),
]
