from django.urls import path
from base.modules.configuracion.views import *

urlpatterns = [
    path('', ConfigurationListView.as_view(), name='configuracion'),
    path('conforden/', ConfigurationOrdenListView.as_view(), name='conforden'),
    path('confpaquete/', ConfigurationPaqueteListView.as_view(), name='confpaquete'),
    path('confpallet', ConfigurationPalletListView.as_view(), name='confpallet'),
    path('confcontenedor', ConfigurationContenedorListView.as_view(), name='confcontenedor'),
    path('confsms', ConfiguracionHistorialSMSListView.as_view(), name='confsms'),
]
