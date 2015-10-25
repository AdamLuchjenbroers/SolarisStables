import os, sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/solaris')
sys.path.append('/var/www/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.grayson'

application = get_wsgi_application()