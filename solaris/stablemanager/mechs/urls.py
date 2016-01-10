from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StableMechsView.as_view(), name='stable_mechs_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableMechsView.as_view(), name='stable_mechs'),

    url(r'^repair/', include('solaris.stablemanager.repairs.urls')),
)
