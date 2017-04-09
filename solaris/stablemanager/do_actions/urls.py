from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StableActionView.as_view(), name='stable_actions_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableActionView.as_view(), name='stable_actions'),

    url(r'^(?P<week>[0-9]+)/list$', views.StableActionListPart.as_view(), name='stable_actions_list'),
    url(r'^(?P<week>[0-9]+)/add$', views.StableActionFormView.as_view(), name='stable_add_action'),
)
