# -*- coding: iso-8859-1 -*-
from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^techtree/?$', 'solaris.cms.views.util_redirect', {'path': '/reference/techtree/'}),
    (r'^techtree/(?P<technology>[^/]+)/', 'solaris.warbook.techtree.views.display_technology', {'selected': '/techtree/'}),
    (r'^/?$', 'solaris.cms.views.news_page', {'selected': '/'}),
    (r'^postnews/?$', 'solaris.cms.views.post_news_page'),
    (r'^login/?$', 'solaris.userforms.views.login_page'),
    (r'^logout/?$', 'solaris.userforms.views.logout_user'),
    (r'^register/?$', 'solaris.userforms.views.registration_page'),
    (r'^reference/', include('solaris.warbook.urls')),
)

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
# Add this entry last - if it isn't matched to a specific app, see if we have it as static content.
urlpatterns += patterns('',
    (r'^(?P<selected>.*)$', 'solaris.cms.views.static_content')
)
