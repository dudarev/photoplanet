"""
Test settings and globals which allow us to run our test suite locally.
"""

from .base import *

CUSTOM_HEADLINE = False
INCLUDE_ANALYTICS = False

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
