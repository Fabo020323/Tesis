import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = 'django-insecure-2xqrwaufxnvz-gkw((47kbm6b=7xsk+e53bso4-^rh_2*p+#ta'

DEBUG = os.getenv("DJANGO_DEBUG") == 'True'

SITE_DOMAIN = os.getenv("SITE_DOMAIN")

HTTPS = os.getenv("HTTPS")

PORT = os.getenv('SITE_PORT')

ALLOWED_HOSTS = [f'{SITE_DOMAIN}']

SESSION_COOKIE_SECURE = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if HTTPS == 'https':
    CSRF_TRUSTED_ORIGINS = [f'https://{SITE_DOMAIN}']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.UsuarioActividadMiddleware',
]

AUTH_USER_MODEL = 'base.CustomUser'

ROOT_URLCONF = 'base_Fabian.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base_Fabian.context.custom_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'base_Fabian.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'base'

LOGOUT_REDIRECT_URL = 'login'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'base/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
