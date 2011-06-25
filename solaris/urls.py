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
    (r'^admin/', include(admin.site.urls)),
    (r'^mechs/$', 'solaris.view.StaticPage.render',{'selected': '/mechs', 'content': 'Mechs!' }),
    (r'^rules/$', 'solaris.view.StaticPage.render',{'selected': '/rules', 'content': 'Rules!' }),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# On the Apache server, this is done using an aliased directory
if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
