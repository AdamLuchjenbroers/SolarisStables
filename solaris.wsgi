import os, sys
sys.path.append('/usr/local/django')
sys.path.append('/usr/local/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.grayson'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
