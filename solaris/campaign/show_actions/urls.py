from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^/?$', views.CampaignActionsView.as_view(), name='campaign_actions_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.CampaignActionsView.as_view(), name='campaign_actions'),

    url(r'^(?P<week>[0-9]+)/list$', views.CampaignActionsListPart.as_view(), name='campaign_actions_listpart'),

    url(r'^(?P<week>[0-9]+)/start$', views.AjaxSetWeekStarted.as_view(), name='campaign_actions_start'),
)    
