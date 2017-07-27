from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^/?$', views.CampaignOverview.as_view(), name='campaign_overview_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.CampaignOverview.as_view(), name='campaign_overview'),

    url(r'^create/?$', views.AjaxCreateCampaignView.as_view()),

    url(r'^actions/', include('solaris.campaign.show_actions.urls')),
    url(r'^fights/', include('solaris.campaign.roster.urls')),
)    
