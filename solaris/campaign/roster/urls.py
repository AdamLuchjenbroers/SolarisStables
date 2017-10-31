from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^/?$', views.FightRosterView.as_view(), name='campaign_fights_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.FightRosterView.as_view(), name='campaign_fights'),
    url(r'^(?P<week>[0-9]+)/add/?$', views.AddFightFormView.as_view(), name='campaign_add_fights'),
)
