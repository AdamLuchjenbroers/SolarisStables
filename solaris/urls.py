# -*- coding: iso-8859-1 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from solaris import settings
from solaris.cms.models import StaticContent

admin.autodiscover()

navigation_options = [(page.title,page.url) for page in StaticContent.objects.all()]

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

for page in StaticContent.objects.all():
  urlpatterns += patterns('',
    (r'^%s$' % page.url[1:], 'solaris.cms.views.static_content',{'selected': page.url, 'content': page.content }),    
)

# Make static content work using the Django dev server.
# On the Apache server, this is done using an aliased directory
if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
