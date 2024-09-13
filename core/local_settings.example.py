import os

# Configuration of project in settings.py is overridden here

ALLOWED_HOSTS = ["*"]
DEBUG = True


# Database configuration


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}

# Host configuration

HOST = "http://localhost:8000"

FRONT_REDIRECT_URL = "https://domain-name/auth/verify/"
MODERATION_HOST = "https://domain-name.uz"

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
#         "KEY_PREFIX": "lenta",
#     },
#     "qr-code": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "qr-code-cache",
#         "TIMEOUT": 3600,
#     },
# }
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# # CELERY
# BROKER_URL = "amqp://localhost"
# CELERY_RESULT_BACKEND = "rpc://"
# CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_AMQP_TASK_RESULT_EXPIRES = 1000
# CELERY_TIMEZONE = "Asia/Tashkent"
