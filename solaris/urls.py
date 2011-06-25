# -*- coding: iso-8859-1 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from solaris import settings

admin.autodiscover()

navigation_options = [
  ('Main','/'),
  ('Mech Lists','/mechs'),
  ('Rules','/rules')
]

urlpatterns = patterns('',
    # Example:
    (r'^$', 'solaris.view.StaticPage.render',{'selected': '/', 'content': 'Coming Soon' }),
    (r'^mechs/$', 'solaris.view.StaticPage.render',{'selected': '/mechs', 'content': 'Mechs!' }),
    (r'^rules/$', 'solaris.view.StaticPage.render',{'selected': '/rules', 'content': 'Rules!' }),
    (r'^admin/', include(admin.site.urls)),
)

# Make static content work using the Django dev server.
# On the Apache server, this is done using an aliased directory
if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
