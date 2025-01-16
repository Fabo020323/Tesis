import os
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from base.errors import *
from base.views import *
from base_Fabian import settings

urlpatterns = [
    path('', include('base.urls')),
]

if os.environ.get('DJANGO_DEBUG', '') != 'False':
    urlpatterns += [path('admin/', admin.site.urls),]

handler404 = error_404_view
handler500 = error_500_view
handler403 = error_404_view
handler400 = error_400_view
handler405 = error_405_view

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
