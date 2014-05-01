from django.conf.urls import patterns

from .views import ReferenceView
from solaris.warbook.techtree.views import TechnologyListView, TechnologyDetailView
from solaris.warbook.pilotskill.views import DisciplineListView, DisciplineDetailView

urlpatterns = patterns('',
    (r'^/?$', ReferenceView.as_view() ), 
    (r'^techtree/?$',  TechnologyListView.as_view() ),
    (r'^techtree/(?P<technology>[^/]+)/?$', TechnologyDetailView.as_view() ),
    (r'^pilotskills/?$', DisciplineListView.as_view() ),
    (r'^pilotskills/(?P<discipline>[^/]+)/?$', DisciplineDetailView.as_view() ),
    (r'^mechs/?$', ReferenceView.as_view()) ,
    (r'^mechs/(?P<name>[^/]+)/?$', ReferenceView.as_view()) ,
    (r'^mechs/(?P<name>[^/]+)/(?P<code>[^/]+)?$', ReferenceView.as_view()) ,    
)