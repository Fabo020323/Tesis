from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from base.modules.usuario.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('theme_color_scheme', 'layout_mode', 'layout_width', 'topbar_color', 'menu_color',
                           'menu_icon', 'imagen', 'sidenav_size', 'sidebar_user_info', 'sidenav_twocolumn', 'sucursales','telefono')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

