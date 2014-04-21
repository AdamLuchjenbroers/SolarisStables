import os, sys
import django.core.handlers.wsgi

sys.path.append('/var/www/solaris')
sys.path.append('/var/www/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.grayson'

application = django.core.handlers.wsgi.WSGIHandler()
