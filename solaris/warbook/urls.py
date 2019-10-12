from django.conf.urls import include, url

from .views import ReferenceView
from solaris.warbook.techtree.views import TechnologyListView, TechnologyDetailView
from solaris.warbook.pilotskill.views import DisciplineListView, DisciplineDetailView, TraitsListView, TraitsDetailView
from solaris.warbook.mech.views import MechListView, MechDetailView, MechSearchView, MechSearchResultsView 

urlpatterns = [
    url(r'^$', ReferenceView.as_view() ), 
    url(r'^techtree/?$',  TechnologyListView.as_view(), name='tech_list' ),
    url(r'^techtree/(?P<slug>[^/]+)/?$', TechnologyDetailView.as_view(), name='technology' ),
    url(r'^pilot-skills/?$', DisciplineListView.as_view(), name='pilot_skills' ),
    url(r'^pilot-skills/(?P<slug>[^/]+)/?$', DisciplineDetailView.as_view(), name='pilot_skill_detail' ),
    url(r'^pilot-issues/?$', TraitsDetailView.as_view(), {'slug' : 'pilot-issues' }, name='pilot_issues', ),

    url(r'^mechs/', include('solaris.warbook.mech.urls')),

    url(r'^ajax/?', include('solaris.warbook.ajax_urls')),    
]
