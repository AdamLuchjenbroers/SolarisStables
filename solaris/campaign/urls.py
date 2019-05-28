from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^create/?$', views.AjaxCreateCampaignView.as_view()),
)    
