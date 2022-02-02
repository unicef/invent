import os
import datetime
import sys

from environs import Env
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*']

PROJECT_NAME = env.str('PROJECT_NAME', default='Example')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default='john@example.org')
# Developer email who can be reached for API inquiries
API_MAINTAINER = env.str('API_MAINTAINER', default='john@example.org')

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'azure',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'drf_yasg',
    'ordered_model',
    'rosetta',
    'adminsortable2',
    'corsheaders',
    'djcelery_email',
    'simple_history',
    'sorl.thumbnail',
    'user',
    'core',
    'project',
    'country',
    'search',
    'scheduler',
    'simple-feedback',
    'import_export',
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ExceptionLoggingMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'tiip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.from_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'tiip.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': env.str('DATABASE_URL', default='postgres'),
        'PORT': 5432,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
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

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('pt', _('Portuguese')),
)
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/django/static'

MEDIA_ROOT = '/usr/share/django/media'
# MEDIA_ROOT = '/usr/share/nginx/html/media'
MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0o644

SITE_ID = env.int('SITE_ID', default=1)
CI_RUN = env.bool('CI_RUN', default=False)

CORS_ORIGIN_ALLOW_ALL = True

# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'user.authentication.BearerTokenAuthentication'
    ),
}


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_profile_id': user.userprofile.id if hasattr(user, 'userprofile') else None,
        'account_type': user.userprofile.account_type if hasattr(user, 'userprofile') else None,
        'is_superuser': user.is_superuser
    }


JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': jwt_response_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Token',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7)
}

# django-allauth and rest-auth settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'user.serializers.ProfileJWTSerializer',
    # 'PASSWORD_RESET_SERIALIZER': 'user.serializers.PasswordResetHTMLEmailSerializer'
}

SOCIALACCOUNT_PROVIDERS = {
    'azure': {
        'APP': {
            'client_id': env.str('AZURE_CLIENT_ID', default=''),
            'secret': env.str('AZURE_SECRET', default=''),
        },
    }
}
SOCIALACCOUNT_ADAPTER = 'user.adapters.MyAzureAccountAdapter'
SOCIALACCOUNT_AZURE_TENANT = env.str('AZURE_TENANT', default='')
SOCIALACCOUNT_CALLBACK_URL = env.str('AZURE_CALLBACK_URL', default='http://localhost/accounts/azure/login/callback/')
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_ADAPTER = 'user.adapters.DefaultAccountAdapterCustom'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False  # This is for backwards compat, should move to True to not store it in DB

ENABLE_API_REGISTRATION = env.bool('ENABLE_API_REGISTRATION', default=True)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_SENDING_PRODUCTION = env.bool('EMAIL_SENDING_PRODUCTION', default=False)

REDIS_URL = env.str('REDIS_URL', default='redis')

# Celery settings
BROKER_URL = 'redis://{}:6379/0'.format(REDIS_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

FROM_EMAIL = DEFAULT_FROM_EMAIL

# Geodata settings
GEOJSON_TEMP_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'temp/')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/logger.log',
            'maxBytes': 10000000,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/login/'

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_MESSAGES_PER_PAGE = 25

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'translations'),  # don't move this, update_translations mgmt cmd is using it
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'core/locale'),
    os.path.join(BASE_DIR, 'country/locale'),
    os.path.join(BASE_DIR, 'project/locale'),
    os.path.join(BASE_DIR, 'search/locale'),
    os.path.join(BASE_DIR, 'user/locale'),
]

for arg in sys.argv:
    if 'test' in arg:
        DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
        PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

if CI_RUN:
    STATIC_ROOT = "/home/circleci/tiip/nginx/site/static/"
    MEDIA_ROOT = "/home/circleci/tiip/django/media/"

OSM_MAP_CLI_KEY = env.str('OSM_MAP_CLI_KEY', default='')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
REDOC_SETTINGS = {
   'LAZY_RENDERING': False
}

PORTFOLIO_PROBLEMSTATEMENT_TRESHOLDS = {
    'MODERATE': 1,
    'HIGH': 6
}

NOTIFICATION_PROJECT_REVIEW_DAYS = 30
MIGRATE_PHASES = env.bool('MIGRATE_PHASES', default=False)

THUMBNAIL_PRESERVE_FORMAT = False
THUMBNAIL_PADDING = True
# THUMBNAIL_RATIO = 14.56/9
THUMBNAIL_HEIGHT = 520
# THUMBNAIL_WIDTH = round(THUMBNAIL_HEIGHT*THUMBNAIL_RATIO)

SIMPLE_FEEDBACK_SEND_TO = env.str('SIMPLE_FEEDBACK_SEND_TO', default='john@example.org')

ENVIRONMENT_NAME = f"DEVELOPMENT - ({env.str('DEPLOY_VERSION', default='Unknown')})"
ENVIRONMENT_COLOR = "blue"

# Validator for emails that can be registered as team members, viewers, eg.: r'(example.org|example.com)$'
EMAIL_VALIDATOR_REGEX = r'{}'.format(env.str('EMAIL_VALIDATOR_REGEX', default=''))

try:
    from .settings_deployed import *  # noqa
except ImportError:
    pass
