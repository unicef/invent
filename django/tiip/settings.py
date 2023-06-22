import os
import datetime
import sys

from environs import Env
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()
ENVIRONMENT = os.environ.get('ENVIRONMENT', default='local')
if ENVIRONMENT:
    env.read_env(path=".env." + ENVIRONMENT)
else:
    env.read_env(path=".env.local")

if ENVIRONMENT == "dev":
    SITE_ID = 2
    env_name = "DEVELOPMENT"
    env_color = "blue"
elif ENVIRONMENT == "tst":
    SITE_ID = 3
    env_name = "TEST"
    env_color = "green"
elif ENVIRONMENT == "uat":
    SITE_ID = 5
    env_name = "UAT"
    env_color = "orange"
elif ENVIRONMENT == "prd":
    SITE_ID = 4
    env_name = "PRODUCTION"
    env_color = "red"
else:
    SITE_ID = 1
    env_name = "LOCAL"
    env_color = "purple"

SECRET_KEY = os.environ.get(
    'SECRET_KEY', default='thisisthedefaultkeyforlocalenv')

DEBUG = env.str('DEBUG', default=False)

ALLOWED_HOSTS = ['*']

PROJECT_SHORT_NAME = env.str('PROJECT_SHORT_NAME', default='Short Name')
PROJECT_NAME = env.str('PROJECT_NAME', default='Example')
SITE_URL = env.str('SITE_URL', default='localhost')
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
    'jsoneditor',
    'user',
    'import_export_celery',
    'core',
    'project',
    'country',
    'search',
    'scheduler',
    'kpi',
    'simple-feedback',
    "dj_anonymizer",
    'import_export',
    'health_check',
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
    'author.middlewares.AuthorDefaultBackendMiddleware',
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
        'NAME': env.str('DATABASE_NAME', default='postgres'),
        'USER': env.str('POSTGRES_USER', default='postgres'),
        'HOST': env.str('DATABASE_HOST', default='postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='postgres'),
        'PORT': 5432,
    }
}

REDIS_URL = env.str('REDIS_URL', default='redis')
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/1".format(REDIS_URL),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
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
MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0o644

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
            'client_id': os.environ.get('AZURE_CLIENT_ID', default=''),
            'secret': os.environ.get('AZURE_SECRET', default=''),
        },
    }
}
SOCIALACCOUNT_ADAPTER = 'user.adapters.MyAzureAccountAdapter'
SOCIALACCOUNT_AZURE_TENANT = os.environ.get('AZURE_TENANT', default='')
SOCIALACCOUNT_CALLBACK_URL = env.str(
    'AZURE_CALLBACK_URL', default='http://localhost/accounts/azure/login/callback/')
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_ADAPTER = 'user.adapters.DefaultAccountAdapterCustom'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
# This is for backwards compat, should move to True to not store it in DB
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False


# List of user parameters to select
AZURE_USER_PARAMETERS = ['id', 'businessPhones', 'country', 'department', 'displayName', 'givenName',
                         'jobTitle', 'mail', 'mobilePhone', 'officeLocation', 'preferredLanguage', 'surname', 'userPrincipalName']

MICROSOFT_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'
MICROSOFT_GRAPH_USERS_URL = f'{MICROSOFT_GRAPH_BASE_URL}/users'
MICROSOFT_GRAPH_SUBSCRIPTION_URL = f'{MICROSOFT_GRAPH_BASE_URL}/subscriptions'


def generate_azure_users_url(user_params: list, top: int = 100) -> str:
    """
    Generates a URL for fetching users from Azure Active Directory.

    Parameters
        user_params (list): The list of parameters to select for each user.
        top (int, optional): The maximum number of users to fetch at a time.

    Returns
        str: The generated URL.
    """
    # Join parameters into a single string
    select_params = ','.join(user_params)
    # Add pagination
    url = f'{MICROSOFT_GRAPH_USERS_URL}?$select={select_params}&$top={top}'
    return url


AZURE_GET_USERS_URL = generate_azure_users_url(AZURE_USER_PARAMETERS)

ENABLE_API_REGISTRATION = env.str('ENABLE_API_REGISTRATION', default=True)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_SENDING_PRODUCTION = env.str('EMAIL_SENDING_PRODUCTION', default=False)

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
    # don't move this, update_translations mgmt cmd is using it
    os.path.join(BASE_DIR, 'translations'),
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

OSM_MAP_CLI_KEY = os.environ.get('OSM_MAP_CLI_KEY', default='')

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

SIMPLE_FEEDBACK_SEND_TO = env.str(
    'SIMPLE_FEEDBACK_SEND_TO', default='john@example.org')

ENVIRONMENT_NAME = f"{env_name} - ({env.str('DEPLOY_VERSION', default='Unknown')})"
ENVIRONMENT_COLOR = env_color

# Validator for emails that can be registered as team members, viewers, eg.: r'(example.org|example.com)$'
EMAIL_VALIDATOR_REGEX = r'{}'.format(
    env.str('EMAIL_VALIDATOR_REGEX', default=''))

# Import the setting_azure settings only in the Azure environments
if ENVIRONMENT in ["dev", "tst", "uat", "prd"]:
    from .settings_deployed import *

# Azure Monitor OpenTelemetry
# if ENVIRONMENT in ['dev']:
#     from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
#     from opentelemetry import trace
#     from opentelemetry.sdk.trace.export import BatchSpanProcessor
#     from opentelemetry.sdk.trace import TracerProvider

#     # Fetch the connection string from the environment variable
#     APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get(
#         'APPLICATIONINSIGHTS_CONNECTION_STRING', default='')

#     if APPLICATIONINSIGHTS_CONNECTION_STRING:
#         trace.set_tracer_provider(TracerProvider())
#         tracer = trace.get_tracer(__name__)

#         exporter = AzureMonitorTraceExporter(
#             connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
#         )

#         trace.get_tracer_provider().add_span_processor(
#             BatchSpanProcessor(exporter)
#         )