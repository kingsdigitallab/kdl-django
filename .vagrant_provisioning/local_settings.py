import getpass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kdl',
        'USER': 'kdl',
        'PASSWORD': 'kdl',
        'ADMINUSER': 'postgres',
        'HOST': 'localhost'
    },
}

INTERNAL_IPS = ('0.0.0.0', '127.0.0.1', '::1')

SECRET_KEY = '12345'

FABRIC_USER = getpass.getuser()

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False

# These are in local because they rely on a locally
# installed binary
CAPTCHA_FLITE_PATH = '/usr/bin/flite'
CAPTCHA_SOX_PATH = '/usr/bin/sox'
