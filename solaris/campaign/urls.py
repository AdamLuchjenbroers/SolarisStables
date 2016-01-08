from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^/?$', views.CampaignOverview.as_view(), name='campaign_overview'),
)    
