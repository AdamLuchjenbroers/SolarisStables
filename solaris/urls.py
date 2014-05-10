# -*- coding: iso-8859-1 -*-
from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings

from .views import SolarisView
from solaris.userforms.views import SolarisLoginView, SolarisRegistrationView

admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', 'solaris.cms.views.news_page', {'selected': '/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^postnews/?$', 'solaris.cms.views.post_news_page'),
    (r'^login/?$', SolarisLoginView.as_view()),
    (r'^logout/?$', 'solaris.userforms.views.logout_user'),
    (r'^register/?$', SolarisRegistrationView.as_view()),
    (r'^reference/?', include('solaris.warbook.urls')),
    (r'^stable/?', include('solaris.stablemanager.urls')),
    (r'^viewtest/?', SolarisView.as_view() )
)

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
# Add this entry last - if it isn't matched to a specific app, see if we have it as static content.
urlpatterns += patterns('',
    (r'^(?P<selected>.*)$', 'solaris.cms.views.static_content')
)
