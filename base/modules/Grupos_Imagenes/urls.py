from django.urls import path
from base.modules.Grupos_Imagenes.views import *

urlpatterns = [
    path('', GrupoListView.as_view(), name='lista_de_grupo'),
    path('crear/', GrupoCreateView.as_view(), name='crear_grupo'),
    path('actualizar/<int:pk>/', GrupoUpdateView.as_view(), name='actualizar_grupo'),
    path('eliminar/<int:pk>', GrupoDeleteView.as_view(), name='eliminar_grupo'),
    path('grupo_plano/<int:pk>/', ExtraerTextoGrupoPlanoView.as_view(), name='grupo_plano'),
    path('imagenes_grupo/<int:pk>/', ListImagenesGruposView.as_view(), name='imagenes_grupo'),
    path('reportes/grupo/<int:grupo_id>/pdf/', ReporteImagenesPDFView.as_view(), name='reporte_imagenes_pdf'),
]
