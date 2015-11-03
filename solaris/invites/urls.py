from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    url(r'^send-invite/$', views.SolarisSendInvite.as_view(),
        name='send-invite'),

    url(r'^accept-invite/(?P<key>\w+)/$', views.SolarisAcceptInvite.as_view(),
        name='accept-invite'),
)
