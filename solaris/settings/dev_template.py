#
# Import all base environment settings
#
from .base import *

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

DATABASES = {
  'default' : {
    'ENGINE'   : 'django.db.backends.postgresql_psycopg2'
  , 'NAME'     : 'database'
  , 'USER'     : 'db user'
  , 'PASSWORD' : 'db password'
  , 'HOST'     : 'db IP address'
  }
}

BASE_DIR = '/home/notavi/Programming/Solaris/SolarisStables'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = '%s/static/' % BASE_DIR
STATIC_URL = '/static/'
USE_DJANGO_STATIC = True 

MEDIA_ROOT = ''
MEDIA_URL = ''

# Path to Solaris Skunkwerks mech files
SSW_STOCK_MECHS_ROOT = '/path/to/ssw/mech/files/'
SSW_UPLOAD_MECHS_ROOT = '/path/to/ssw/upload/folder/'
SSW_UPLOAD_TEMP = '/var/tmp/ssw/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Dump a random, reasonably long string of junk here'

TEMPLATES = [
  {
    'BACKEND' : 'django.template.backends.django.DjangoTemplates' 
  , 'DIRS' : [ '%s/solaris/templates/' % BASE_DIR, ] 
  , 'APPDIRS' : True
  , 'OPTIONS' : {
      'debug' : True
    , 'context_processors' : SOLARIS_TEMPLATE_PROCESSORS
    }
  } 
]

EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = 'yes'
EMAIL_HOST_USER = 'account@example.com'
EMAIL_HOST_PASSWORD = 'password'

DEFAULT_FROM_EMAIL = 'account@example.com'

CURRENT_CAMPAIGN='Solaris7'
