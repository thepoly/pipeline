from .base import *

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

try:
    from .local import *
except ImportError:
    pass
