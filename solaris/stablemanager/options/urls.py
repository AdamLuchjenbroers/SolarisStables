
from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StableOptionsView.as_view(), name='stable_options_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableOptionsView.as_view(), name='stable_options'),
)
