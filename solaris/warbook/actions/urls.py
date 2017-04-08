from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.ActionGroupListView.as_view(), name='actions'),
    url(r'^(?P<slug>[^/]+)/?$', views.ActionGroupDetailView.as_view(), name='action_group_detail' ),

    url(r'^(?P<pk>[0-9]+)/json', views.ActionDetailJsonView.as_view(), name='action_jsondata')
)
