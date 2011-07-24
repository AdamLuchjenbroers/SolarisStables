# -*- coding: iso-8859-1 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from solaris import settings
from solaris.cms.models import StaticContent

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^techtree/?$', 'solaris.warbook.views.list_technologies', {'selected': '/techtree/'}),
    (r'^techtree/(?P<technology>[^/]+)/', 'solaris.warbook.views.display_technology', {'selected': '/techtree/'}),
    ('^login/?$', 'solaris.userforms.views.login_page'),
    ('^logout/?$', 'solaris.userforms.views.logout_user'),
    ('^register/?$', 'solaris.userforms.views.registration_page'),
)

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
# Add this entry last - if it isn't matched to a specific app, see if we have it as static content.
urlpatterns += patterns('',
    (r'^(?P<selected>.*)$', 'solaris.cms.views.static_content')
)
