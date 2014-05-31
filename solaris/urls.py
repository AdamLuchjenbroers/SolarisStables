# -*- coding: iso-8859-1 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from solaris.userforms.views import SolarisLoginView, SolarisRegistrationView
from solaris.cms.views import NewsListView, NewsPostFormView

admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', NewsListView.as_view()),
    
    (r'^postnews/?$', NewsPostFormView.as_view()),
    url(r'^login/?$', SolarisLoginView.as_view(), name='login'),
    (r'^logout/?$', 'solaris.userforms.views.logout_user'),
    url(r'^register/?$', SolarisRegistrationView.as_view(), name='register'),
    
    (r'^admin/', include(admin.site.urls)),
    (r'^reference/', include('solaris.warbook.urls')),
    (r'^stable/', include('solaris.stablemanager.urls'))
)

if settings.USE_DJANGO_STATIC:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

