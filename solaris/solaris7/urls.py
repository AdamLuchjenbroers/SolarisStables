
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<campaign_url>[A-Za-z0-9]+)/?$', views.Solaris7Overview.as_view(), name='campaign_overview_now'),
    url(r'^(?P<campaign_url>[A-Za-z0-9]+)/(?P<week>[0-9]+)/?$', views.Solaris7Overview.as_view(), name='campaign_overview'),

    url(r'^(?P<campaign_url>[A-Za-z0-9]+)/actions/', include('solaris.solaris7.show_actions.urls')),
    url(r'^(?P<campaign_url>[A-Za-z0-9]+)/fights/', include('solaris.solaris7.roster.urls')),
    url(r'^(?P<campaign_url>[A-Za-z0-9]+)/tools/', include('solaris.campaign.tools.urls')),

    url(r'^fight-info/', include('solaris.solaris7.fightinfo.urls')),
)    
