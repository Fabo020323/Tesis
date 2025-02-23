import os

from django.db.models.signals import post_migrate
from django.dispatch import receiver, Signal
from base.modules.configuracion.models import Configuracion
from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


@receiver(post_migrate)
def create_default_configurations(sender, **kwargs):
    #return 0
    default_configs = {
        "paginado": int(os.environ.get('PAGINATE')),
        "version": str(os.environ.get('VERSION')),
    }
    for key, value in default_configs.items():
        Configuracion.objects.get_or_create(llave=key, defaults={'valor': value})

    for model in apps.get_models():
        ContentType.objects.get_for_model(model)

    for app_config in apps.get_app_configs():
        create_permissions(app_config, verbosity=0)


