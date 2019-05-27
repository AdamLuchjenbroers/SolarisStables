from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^/?$', views.CampaignOverview.as_view(), name='campaign_overview_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.CampaignOverview.as_view(), name='campaign_overview'),

    url(r'^create/?$', views.AjaxCreateCampaignView.as_view()),

    url(r'^actions/', include('solaris.solaris7.show_actions.urls')),
    url(r'^fights/', include('solaris.solaris7.roster.urls')),
    url(r'^tools/', include('solaris.campaign.tools.urls')),
)    
