from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^create/?$', views.AjaxCreateCampaignView.as_view()),
] 
