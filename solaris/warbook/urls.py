from django.conf.urls import patterns

from .views import ReferenceView
from solaris.warbook.techtree.views import TechnologyListView, TechnologyDetailView
from solaris.warbook.pilotskill.views import DisciplineListView, DisciplineDetailView
from solaris.warbook.mech.views import MechListView, MechDetailView, MechSearchView, MechSearchResultsView 

urlpatterns = patterns('',
    (r'^/?$', ReferenceView.as_view() ), 
    (r'^techtree/?$',  TechnologyListView.as_view() ),
    (r'^techtree/(?P<technology>[^/]+)/?$', TechnologyDetailView.as_view() ),
    (r'^pilotskills/?$', DisciplineListView.as_view() ),
    (r'^pilotskills/(?P<discipline>[^/]+)/?$', DisciplineDetailView.as_view() ),
    (r'^mechs/?$', MechSearchView.as_view()) ,
    (r'^mechs/search/?$', MechSearchResultsView.as_view())
    (r'^mechs/(?P<name>[^/]+)/?$', MechListView.as_view()) ,
    (r'^mechs/(?P<name>[^/]+)/(?P<code>[^/]+)/?$', MechDetailView.as_view()) ,    
)