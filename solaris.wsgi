import os, sys
sys.path.append('/var/www/solaris')
sys.path.append('/usr/local/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
