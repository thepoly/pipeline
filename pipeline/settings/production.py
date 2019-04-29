import os

from .base import *

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "poly.rpi.edu"]

DATABASES["default"]["CONN_MAX_AGE"] = 600

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "django.server",
        }
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"], "propagate": False}
    },
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
