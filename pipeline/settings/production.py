import os

from .base import *

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "poly.rpi.edu"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pipeline",
        "HOST": "postgres",
        "PORT": "5432",
        "USER": "pipeline",
        "PASSWORD": "pipeline",
    }
}

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
        "OPTIONS": {
            "MAX_ENTRIES": 1000  # This is just a guess and should eventually be supported by metrics
        },
    }
}

try:
    from .local import *
except ImportError:
    pass
