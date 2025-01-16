import os
import pytz
from datetime import datetime
import random
from django.core.exceptions import ObjectDoesNotExist
from ..base.modules.configuracion.models import Configuracion

def mes_en_espannol(mes_numero):
    meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }
    return meses.get(mes_numero, '')


def get_config_value(key, default):
    try:
        return Configuracion.objects.get(llave=key).valor
    except ObjectDoesNotExist:
        return default


def get_order_generate():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(3))


def update_paginate():
    return int(get_config_value("paginado", int(os.environ.get('PAGINATE'))))




