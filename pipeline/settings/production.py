import os

from .base import *

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "poly.rpi.edu"]

try:
    from .local import *
except ImportError:
    pass
