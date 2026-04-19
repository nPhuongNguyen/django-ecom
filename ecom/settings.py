import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

# 1. INITIALIZATION
# ----------------------------------------------------------------------
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. CORE SETTINGS
# ----------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure--hchd8vtd!q0xl-z+mu@4&n%!uax+)d1p$7i7ti$rvc#h@#3^l')
TOKEN_SECRET_KEY = os.environ.get("TOKEN_SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "True") == "True"
IS_DEV = int(os.environ.get('IS_DEV', 0))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# URL Configuration
PREFIX_URL = os.environ.get("PREFIX_URL", "")
API_VERSION = os.environ.get("API_VERSION", "v1")
ROOT_URLCONF = 'ecom.urls_base'
WSGI_APPLICATION = 'ecom.wsgi.application'
APPEND_SLASH = False

# 3. APPS & MIDDLEWARE
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'storages',
    'apps.catalogue',
    'apps.auths',
    'apps.accounts',
    'apps.shared',
]

MIDDLEWARE = [
    "apps.middleware.request_middleware.RequestMiddleware",
]

# 4. DATABASES
# ----------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT", "3306"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# 5. CACHES (REDIS)
# ----------------------------------------------------------------------
def get_redis_url(prefix="REDIS"):
    host = os.getenv(f"{prefix}_HOST")
    port = os.getenv(f"{prefix}_PORT")
    db = os.getenv(f"{prefix}_DB")
    password = os.getenv(f"{prefix}_PASSWORD")
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_redis_url("REDIS"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "ecom_cache"
    },
    "auth": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_redis_url("REDIS_AUTH"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "ecom_auth_cache"
    }
}

# 6. CELERY & MESSAGE BROKERS
# ----------------------------------------------------------------------
# Celery
CELERY_BROKER_URL = get_redis_url("REDIS")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = None
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_EXTENDED = False

# Kafka
LIST_BROKERS = os.environ.get('LIST_BROKERS', '').split(',')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_GROUP_LOG = os.environ.get('KAFKA_GROUP_LOG')

# 7. STORAGE (MINIO)
# ----------------------------------------------------------------------
MINIO_ENDPOINT = config("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = config("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = config("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = config("MINIO_BUCKET_NAME")
MINIO_BASE_URL = config("MINIO_BASE_URL")
MINIO_LOCATION = config("MINIO_LOCATION")
MINIO_PORT = config("MINIO_PORT")

STORAGES = {
    "default": {
        "BACKEND": "apps.utils.storages.MinioMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# 8. REST FRAMEWORK CONFIG
# ----------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.shared.drf.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# 9. EMAIL & NOTIFICATIONS
# ----------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == 'True'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

TOKEN_TELEGRAM_BOT = os.environ.get("TOKEN_TELEGRAM_BOT")
CHAT_ID_TELEGRAM_BOT = os.environ.get('CHAT_ID_TELEGRAM_BOT')

# 10. INTERNATIONALIZATION & STATIC
# ----------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = False
USE_L10N = True

LOCALE_PATHS = [BASE_DIR / 'locale']
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]