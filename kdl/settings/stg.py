from .base import *  # noqa

CACHE_REDIS_DATABASE = '1'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = INTERNAL_IPS + ('', )
ALLOWED_HOSTS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_kdl_stg',
        'USER': 'app_kdl',
        'PASSWORD': '',
        'HOST': ''
    },
}


# -----------------------------------------------------------------------------
# Local settings
# -----------------------------------------------------------------------------

try:
    from .local import *  # noqa
except ImportError:
    pass
