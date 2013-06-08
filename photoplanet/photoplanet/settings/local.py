from base import *
from instagram import *

CUSTOM_HEADLINE = False
INCLUDE_ANALYTICS = False


# extending settings for debug toolbar

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'debug_toolbar',
)
