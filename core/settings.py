import os
from pathlib import Path

from datetime import timedelta
from dotenv import load_dotenv

# Path to .env file
dotenv_path = os.path.join(Path(__file__).resolve().parent.parent, ".env")

load_dotenv(dotenv_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=4w6_m%0mw)^zsd&kkzrytua5g+!z8ixxs0fsbw^rgqw@hhym5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ai",
    "campaign",
    "core",
    "common",
    # 3rd-party apps the project depends on
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # noqa
    "social_django",
    "dj_rest_auth",
    "axes",
    "django_resized",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",  # new
    "allauth.account.middleware.AccountMiddleware",
    "axes.middleware.AxesMiddleware",

    # Hitcount views for campaign middleware
    "helpers.middlewares.CampaignViewMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

INTERNAL_IPS = ["127.0.0.1"]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_USE_JWT = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/min",
        "user": "10000/min",
        "loginAttempts": "6/min",
    },
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DATE_FORMAT": "%Y-%m-%d",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=20),
}


AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    # "social_core.backends.facebook.FacebookOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    # # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    "axes.backends.AxesStandaloneBackend"
]


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]



SOCIALACCOUNT_PROVIDERS = {  # noqa
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    # "facebook": {
    #     "METHOD": "oauth2",
    #     "SCOPE": ["email", "public_profile"],
    #     "AUTH_PARAMS": {"auth_type": "reauthenticate"},
    #     "INIT_PARAMS": {"cookie": True},
    #     "FIELDS": [
    #         "id",
    #         "email",
    #         "first_name",
    #         "last_name",
    #         "middle_name",
    #         "name",
    #         "name_format",
    #         "picture",
    #         "short_name",
    #     ],
    #     "EXCHANGE_TOKEN": True,
    #     "VERIFIED_EMAIL": False,
    #     "VERSION": "v7.0",
    # },
    # "telegram": {"TOKEN": "your-token-here"},  # noqa
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "521439139122-t8itloi8g5l7k13bastf0n618nhm9v4i.apps.googleusercontent.com"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

OAUTH_CALLBACK_URL = "http://localhost:3000/auth"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
EMAIL_CONFIRMATION_HMAC = False 
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
LOGIN_URL = "http://localhost:3000/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_TEMPLATE_EXTENSION = "html"
SOCIALACCOUNT_AUTO_SIGNUP = True 


SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)


SWAGGER_SETTINGS = {
    "JSON_EDITOR": True,
}


CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True


AUTH_USER_MODEL = "common.user"


REGISTRATION_EXPIRATION_CODE_MINUTES = 1
VERIFICATION_EXPIRATION_CODE_SECONDS = 86400
REGISTRATION_SEND_CODE_INTERVAL = 120

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")


DJANGORESIZED_DEFAULT_SIZE = [1200, 800]  # noqa
DJANGORESIZED_DEFAULT_QUALITY = 85  # noqa
DJANGORESIZED_DEFAULT_KEEP_META = True  # noqa
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "WEBP"  # noqa
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True  # noqa

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST")  # smtp-relay.sendinblue.com
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"  # False
EMAIL_PORT = os.getenv("EMAIL_PORT")  # 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # your email address
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # your password
DEFAULT_FROM_EMAIL = os.getenv( "DEFAULT_FROM_EMAIL")  # email ending with @sendinblue.com

OAUTH_CALLBACK_URL = "https://lenta.uz/auth"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
EMAIL_CONFIRMATION_HMAC = False  # noqa
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
LOGIN_URL = "https://beta.imkon.uz/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_TEMPLATE_EXTENSION = "html"
SOCIALACCOUNT_AUTO_SIGNUP = True  # noqa


VALID_MOBILE_COUNTRY_CODES = ["998"]
REGISTRATION_SEND_SMS_INTERVAL = 120
REGISTER_ATTEMPTS_LIMIT = 3
VERIFY_ATTEMPTS_LIMIT = 10
REGISTRATION_BAN_MINUTES = 30


try:
    from .local_settings import *  # noqa
except ImportError:
    print(
        "Please create local_settings.py file and configure it using local_settings.example.py file in the core directory."
    )
