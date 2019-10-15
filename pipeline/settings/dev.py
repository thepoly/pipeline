import logging

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "9v281(zz#j15vjq5yvnp(zvn=^=e)h@dfe-uj58#9p9+w&o*tm"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "nplusone.ext.django.NPlusOneMiddleware",
] + MIDDLEWARE

INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar", "nplusone.ext.django"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "formatters": {
        "verbose": {"format": "[{asctime}] {levelname} {name} {message}", "style": "{"}
    },
    "loggers": {
        "nplusone": {"handlers": ["console"], "level": "WARN"},
        "pipeline": {"handlers": ["console"], "level": "DEBUG"},
    },
}


DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://postgres:postgres@127.0.0.1:5432/pipeline"
    )
}


NPLUSONE_LOGGER = logging.getLogger("nplusone")
NPLUSONE_LOG_LEVEL = logging.WARN

# Caching. Use dummy cache in development
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

try:
    from .local import *
except ImportError:
    pass
