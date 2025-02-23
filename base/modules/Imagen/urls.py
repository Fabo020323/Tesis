from django.urls import path
from base.modules.Imagen.views import *

urlpatterns = [
    path('', ImagenListView.as_view(), name='lista_de_imagen'),
    path('crear/', ImagenCreateView.as_view(), name='crear_imagen'),
    path('actualizar/<int:pk>/', ImagenUpdateView.as_view(), name='actualizar_imagen'),
    path('eliminar/<int:pk>', ImagenDeleteView.as_view(), name='eliminar_imagen'),
    path('plano/<int:pk>/', ExtraerTextoViewPlano.as_view(), name='plano'),
    path('ver_plano/<int:pk>/', VerAnalisisPlanoView.as_view(), name='ver_plano'),
    path('formateado/<int:pk>/',ExtraerTextoViewFormateado.as_view(),name='formateado'),
    path('ver_formato/<int:pk>',VerAnalisisFormateadoView.as_view(),name='ver_formato'),
]
