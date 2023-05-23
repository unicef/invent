# PRODUCTION SETTINGS
import datetime
import sentry_sdk
from environs import Env
from celery.schedules import crontab
from sentry_sdk.integrations.django import DjangoIntegration

env = Env()
env.read_env()
sentry_sdk.init(
    dsn=env.str('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    release=env.str('DEPLOY_VERSION', default='0.0.0')
)

EMAIL_HOST = env.str('EMAIL_HOST', default='')
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_PORT = env.str('EMAIL_PORT', default=25)

CELERYBEAT_SCHEDULE = {
    "send_project_approval_digest": {
        "task": 'send_project_approval_digest',
        "schedule": datetime.timedelta(days=1),
    },
    "project_still_in_draft_notification": {
        "task": 'project_still_in_draft_notification',
        "schedule": datetime.timedelta(days=31),
    },
    "published_projects_updated_long_ago": {
        "task": 'published_projects_updated_long_ago',
        "schedule": datetime.timedelta(days=31),
    },
    "project_review_requested_monthly_notification": {
        "task": 'project_review_requested_monthly_notification',
        "schedule": datetime.timedelta(days=30),
    },
    "solution_log_task": {
        "task": "solution_log_task",
        "schedule": crontab(hour=1, minute=0),
    },
    "country_inclusion_log_task": {
        "task": "country_inclusion_log_task",
        "schedule": crontab(hour=1, minute=0),
    },
}

DEBUG = env.str('DEBUG', default='False')
# allowed_hosts = env.str('ALLOWED_HOSTS', default='')
ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
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

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REDIRECT_EXEMPT = [r'^health_check']

# csrf_trusted_origins = env.str('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = ['*']
