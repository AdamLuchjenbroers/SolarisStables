from django.conf.urls import patterns

from .views import ReferenceView
from solaris.warbook.techtree.views import TechnologyListView, TechnologyDetailView

urlpatterns = patterns('',
    (r'^/?$', ReferenceView.as_view() ), 
    (r'^techtree/?$',  TechnologyListView.as_view() ),
    (r'^techtree/(?P<technology>[^/]+)/?$', TechnologyDetailView.as_view() ),
    (r'^pilotskills/?$', 'solaris.warbook.pilotskill.views.list_disciplines'),
    (r'^pilotskills/(?P<discipline>[^/]+)/?$', 'solaris.warbook.pilotskill.views.show_discipline')
    (r'^mechs/?$', ReferenceView.as_view()) ,
    (r'^mechs/(?P<name>[^/]+)/?$', ReferenceView.as_view()) ,
    (r'^mechs/(?P<name>[^/]+)/(?P<code>[^/]+)?$', ReferenceView.as_view()) ,    
)