import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv
load_dotenv()

# CORE
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
TOKEN_SECRET_KEY = os.environ.get("TOKEN_SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# API VERSIONING
PREFIX_URL = os.environ.get("PREFIX_URL")
API_VERSION = os.environ.get("API_VERSION")
IS_DEV = int(os.environ.get('IS_DEV', 0))

DJANGO_APPS = [
    'daphne',
    'channels',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'storages',
    'django_filters',
]

LOCAL_APPS = [
    'apps.catalogue',
    'apps.auths',
    'apps.accounts',
    'apps.shared',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# DATABASE (MySQL)
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "apps.middleware.request_middleware.RequestMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
        },
    },
    "loggers": {
        "o2m-smart-link-api-logging": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },

}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
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
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

APPEND_SLASH = False # Bỏ dấu "/" cuối url

ASGI_APPLICATION = "ecom.asgi.application"

#Redis default
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

#Redis auth
REDIS_AUTH_HOST = os.getenv("REDIS_AUTH_HOST")
REDIS_AUTH_PORT = os.getenv("REDIS_AUTH_PORT")
REDIS_AUTH_DB = os.getenv("REDIS_AUTH_DB")
REDIS_AUTH_PASSWORD = os.getenv("REDIS_AUTH_PASSWORD")

#CACHES (Redis)
def redis_url(host, port, db, password=None):
    if password: return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_url(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "ecom_cache"
    },
    "auth": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_url(REDIS_AUTH_HOST, REDIS_AUTH_PORT, REDIS_AUTH_DB, REDIS_AUTH_PASSWORD),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "ecom_auth_cache"
    }
}

# KAFKA
LIST_BROKERS = os.environ.get('LIST_BROKERS', '').split(',')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_GROUP_LOG = os.environ.get('KAFKA_GROUP_LOG')

# CELERY
CELERY_BROKER_URL = CACHES["default"]["LOCATION"]
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = None
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_EXTENDED = False

# STORAGE (MinIO)
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME")
MINIO_BASE_URL = os.environ.get("MINIO_BASE_URL")
MINIO_LOCATION = os.environ.get("MINIO_LOCATION")
MINIO_PORT = os.environ.get("MINIO_PORT")
MINIO_STORAGE_CONFIG = {
    "ENDPOINT": MINIO_ENDPOINT,
    "ACCESS_KEY": MINIO_ACCESS_KEY,
    "SECRET_KEY": MINIO_SECRET_KEY,
    "BUCKET_NAME": MINIO_BUCKET_NAME,
    "BASE_URL": MINIO_BASE_URL,
    "LOCATION": MINIO_LOCATION,
    "PORT": MINIO_PORT,
}

STORAGES = {
    "default": {"BACKEND": "apps.utils.storages.MinioMediaStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == 'True'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

# TELEGRAM BOT
TOKEN_TELEGRAM_BOT = os.environ.get("TOKEN_TELEGRAM_BOT")
CHAT_ID_TELEGRAM_BOT = os.environ.get('CHAT_ID_TELEGRAM_BOT')
TELEGRAM_CONFIG = {
    "TOKEN": TOKEN_TELEGRAM_BOT,
    "CHAT_ID": CHAT_ID_TELEGRAM_BOT
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [CACHES["default"]["LOCATION"]]
        },
    },
}

ROOT_URLCONF = 'ecom.urls_base'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            ],
        },
    },
]

# Ngôn ngữ mặc định và múi giờ 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True #Dịch ngôn ngữ
USE_TZ = False #Không sử dụng múi giờ
USE_L10N = True #Định dạng ngày tháng theo ngôn ngữ
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'