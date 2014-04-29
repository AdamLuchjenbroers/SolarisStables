# Settings applicable to every environment

TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',   
#     'django.template.loaders.eggs.load_template_source',
)

GENSHI_TEMPLATE_LOADERS = (
     'django_genshi.loaders.filesystem.load_template',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'solaris.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'solaris.cms',
    'solaris.warbook',
    'solaris.warbook.techtree',
    'solaris.warbook.pilotskill',
    'solaris.warbook.mech',
    'solaris.stablemanager',
    'solaris.stablemanager.assets',
    'solaris.battlereport',
    'south',
)
