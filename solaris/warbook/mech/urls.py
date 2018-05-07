from django.conf.urls import patterns, include, url

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.MechSearchView.as_view(), name='mech_search') ,
    url(r'^search/?$', views.MechSearchResultsView.as_view(), name='mech_searchresult'),
    url(r'^(?P<name>[^/]+)/?$', views.MechListView.as_view(), name='mech_chassis') ,
    url(r'^(?P<name>[^/]+)/(?P<code>[^/]+)/(?P<omni>[^/]+)/?$', views.MechDetailView.as_view(), name='mech_detail') ,
    url(r'^(?P<name>[^/]+)/(?P<code>[^/]+)/?$', views.MechDetailView.as_view(), name='mech_detail_base') ,
)
