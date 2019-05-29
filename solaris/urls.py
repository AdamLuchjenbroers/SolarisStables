# -*- coding: iso-8859-1 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import allauth.account.urls

from solaris.account.views import SolarisLoginView, SolarisRegistrationView
from solaris.cms.views import NewsListView, NewsPostFormView

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern

from . import pdf

admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', NewsListView.as_view()),
    
    (r'^postnews/?$', NewsPostFormView.as_view()),
    url(r'^login/?$', SolarisLoginView.as_view(), name='account_login'),
    (r'^logout/?$', 'solaris.account.views.logout_user'),

    url(r'^register/?$', SolarisRegistrationView.as_view(), name='account_signup'),
    
    url('^account/', include('solaris.account.urls')),
    url('^invite/', include('solaris.account.invite_urls', namespace='invitations')),
        
    (r'^admin/', include(admin.site.urls)),
    (r'^reference/', include('solaris.warbook.urls')),
    (r'^stable/', include('solaris.stablemanager.urls')),
    (r'^files/', include('solaris.files.urls')),

    (r'^campaign/', include('solaris.campaign.urls')),
    (r'^solaris/', include('solaris.solaris7.urls')),
    
    (r'^wiki/', get_wiki_pattern()),
    (r'^notify/', get_notify_pattern()),
    
    (r'^markitup/', include('markitup.urls'))
)

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

