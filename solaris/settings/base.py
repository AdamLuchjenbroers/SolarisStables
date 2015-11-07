# Settings applicable to every environment
from django.conf.global_settings import MIGRATION_MODULES

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
#   'solaris.templates.load_from__app'   
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
    "solaris.utils.determine_selected"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'solaris.urls'

WIKI_BASEURL = True

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown'

JQUERY_URL = '/static/js/jquery-1.11.1.js'

MIGRATION_MODULES = {
    'warbook'       : 'solaris.warbook.migrations'
,   'stablemanager' : 'solaris.stablemanager.migrations'
,   'cms'           : 'solaris.cms.migrations'
,   'campaign'      : 'solaris.campaign.migrations'
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'solaris',
    'solaris.cms',
    'solaris.campaign',
    'solaris.warbook',
    'solaris.warbook.techtree',
    'solaris.warbook.pilotskill',
    'solaris.warbook.mech',
    'solaris.warbook.equipment',
#    'solaris.stablemanager',
#    'solaris.stablemanager.assets',
#    'solaris.stablemanager.ledger',
    'markitup',
    #Django-Wiki
    'django_nyt',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'invitations',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
)

ACCOUNT_ADAPTER='invitations.models.InvitationsAdapter'
INVITATIONS_INVITE_ONLY=True
INVITATIONS_INVITATION_EXPIRY=14
