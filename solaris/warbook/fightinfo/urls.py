from django.conf.urls import patterns, include, url

from . import views 

urlpatterns = patterns('',
    url(r'^types/?$', views.FightTypesView.as_view(), name='fightinfo_fighttypes'),
    url(r'^types/(?P<slug>[^/]+)/?$', views.FightTypeDetailView.as_view(), name='fightinfo_detail'),

    url(r'^conditions/?$', views.ConditionsView.as_view(), name='fightinfo_conditions'),
    url(r'^maps/?$', views.MapsView.as_view(), name='fightinfo_maps'),
)
