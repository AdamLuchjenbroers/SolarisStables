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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOLARIS_TEMPLATE_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
#    "sekizai.context_processors.sekizai",
    "solaris.utils.determine_selected",    
#    "allauth.account.context_processors.account",
#    "allauth.socialaccount.context_processors.socialaccount",
]


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
,   'solaris7'      : 'solaris.solaris7.migrations'
,   'files'         : 'solaris.files.migrations'
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
    'solaris.solaris7',
    'solaris.solaris7.fightinfo',
    'solaris.solaris7.roster',
    'solaris.solaris7.actions',
    'solaris.warbook',
    'solaris.warbook.techtree',
    'solaris.warbook.pilotskill',
    'solaris.warbook.mech',
    'solaris.warbook.equipment',
    'solaris.stablemanager',
    'solaris.stablemanager.mechs',
    'solaris.stablemanager.pilots',
    'solaris.stablemanager.ledger',
    'solaris.stablemanager.repairs',
    'solaris.stablemanager.do_actions',
    'solaris.files',
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
    'allauth',
    'allauth.account',
    'allauth.socialaccount'
)

LOGIN_REDIRECT_URL="/"

ACCOUNT_ADAPTER='invitations.models.InvitationsAdapter'
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_LOGIN_REDIRECT_URL="/login"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL="/login"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL="/"

INVITATIONS_INVITE_ONLY=True
INVITATIONS_INVITATION_EXPIRY=14
INVITATIONS_SIGNUP_REDIRECT="/register/"

#Manually specifying the Django 1.7+ Test runner stifles a few 
#dud warnings (seem to be triggered off of unrelated fields).
# https://code.djangoproject.com/ticket/23469
# http://stackoverflow.com/questions/25871261/django-1-7-how-do-i-suppress-1-6-w001-some-project-unittests-may-not-execut
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

