from django.conf.urls import patterns, include, url

from .views import ReferenceView
from solaris.warbook.techtree.views import TechnologyListView, TechnologyDetailView
from solaris.warbook.pilotskill.views import DisciplineListView, DisciplineDetailView
from solaris.warbook.mech.views import MechListView, MechDetailView, MechSearchView, MechSearchResultsView 

urlpatterns = patterns('',
    (r'^/?$', ReferenceView.as_view() ), 
    url(r'^techtree/?$',  TechnologyListView.as_view(), name='tech_list' ),
    url(r'^techtree/(?P<slug>[^/]+)/?$', TechnologyDetailView.as_view(), name='technology' ),
    url(r'^pilotskills/?$', DisciplineListView.as_view(), name='discipline_list' ),
    url(r'^pilotskills/(?P<slug>[^/]+)/?$', DisciplineDetailView.as_view(), name='discipline' ),
    url(r'^mechs/?$', MechSearchView.as_view(), name='mech_search') ,
    url(r'^mechs/search/?$', MechSearchResultsView.as_view(), name='mech_searchresult'),
    url(r'^mechs/(?P<name>[^/]+)/?$', MechListView.as_view(), name='mech_chassis') ,
    url(r'^mechs/(?P<name>[^/]+)/(?P<code>[^/]+)/?$', MechDetailView.as_view(), name='mech_detail') ,
    url(r'^ajax/?', include('solaris.warbook.ajax_urls'))    
)
