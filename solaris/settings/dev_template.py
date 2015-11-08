#
# Import all base environment settings
#
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
  'default' : {
    'ENGINE'   : 'django.db.backends.postgresql_psycopg2'
  , 'NAME'     : 'database'
  , 'USER'     : 'db user'
  , 'PASSWORD' : 'db password'
  , 'HOST'     : 'db IP address'
  }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = '/<source folder>/static/'
STATIC_URL = '/static/'
USE_DJANGO_STATIC = True 

MEDIA_ROOT = ''
MEDIA_URL = ''

# Path to Solaris Skunkwerks mech files
SSW_STOCK_MECHS_ROOT = '/path/to/ssw/mech/files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Dump a random, reasonably long string of junk here'


GENSHI_TEMPLATE_DIRS = (
     '/<source folder>/solaris/templates/'                   
#    '/usr/local/django/solaris/templates/'
)

TEMPLATE_DIRS = (
      '/<source folder>/solaris/templates/'                
#    '/usr/local/django/solaris/templates/'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = 'yes'
EMAIL_HOST_USER = 'account@example.com'
EMAIL_HOST_PASSWORD = 'password'

DEFAULT_FROM_EMAIL = 'account@example.com'