# -*- coding: iso-8859-1 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

import allauth.account.urls

from solaris.account.views import SolarisLoginView, SolarisRegistrationView, SolarisLogoutView
from solaris.cms.views import NewsListView, NewsPostFormView

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern

from . import pdf

admin.autodiscover()

urlpatterns = [
    url(r'^$', NewsListView.as_view()),
    
    url(r'^postnews/?$', NewsPostFormView.as_view()),
    url(r'^login/?$', SolarisLoginView.as_view(), name='account_login'),
    url(r'^logout/?$', SolarisLogoutView.as_view(), name='account_logout'),

    url(r'^register/?$', SolarisRegistrationView.as_view(), name='account_signup'),
    
    url('^account/', include('solaris.account.urls')),
    url('^invite/', include('solaris.account.invite_urls', namespace='invitations')),
        
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reference/', include('solaris.warbook.urls')),
    url(r'^stable/', include('solaris.stablemanager.urls')),
    url(r'^files/', include('solaris.files.urls')),

    url(r'^campaign/', include('solaris.campaign.urls')),
    url(r'^solaris/', include('solaris.solaris7.urls')),
    
    url(r'^wiki/', get_wiki_pattern()),
    url(r'^notify/', get_notify_pattern()),
    
    url(r'^markitup/', include('markitup.urls'))
]

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

