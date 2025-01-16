from datetime import datetime
from base.modules.configuracion.models import Configuracion


def custom_context(request):
    return {
        'site_names': 'DjangoMVT',
        'current_year': datetime.now().year,
        'version': Configuracion.objects.get(llave='version').valor,
        'rastreo': Configuracion.objects.get(llave='rastreo').valor,
        'credito': Configuracion.objects.get(llave='credito').valor,
        'is_user_authenticated': request.user.is_authenticated,
        'user_settings': {
            'theme_color_scheme': request.user.theme_color_scheme if request.user.is_authenticated else None,
            'layout_width': request.user.layout_width if request.user.is_authenticated else None,
            'layout_mode': request.user.layout_mode if request.user.is_authenticated else None,
            'topbar_color': request.user.topbar_color if request.user.is_authenticated else None,
            'menu_color': request.user.menu_color if request.user.is_authenticated else None,
            'menu_icon': request.user.menu_icon if request.user.is_authenticated else None,
            'sidenav_size': request.user.sidenav_size if request.user.is_authenticated else None,
            'sidebar_user_info': request.user.sidebar_user_info if request.user.is_authenticated else None,
            'sidenav_twocolumn': request.user.sidenav_twocolumn if request.user.is_authenticated else None,
        }
    }
