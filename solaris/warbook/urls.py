from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^techtree/?$',  'solaris.warbook.techtree.views.list_technologies', {'selected': '/techtree/'}),
    (r'^techtree/(?P<technology>[^/]+)/?$', 'solaris.warbook.techtree.views.display_technology', {'selected': '/techtree/'}),
    (r'^pilotskills/?$', 'solaris.warbook.pilotskill.views.list_disciplines'),
    (r'^pilotskills/(?P<discipline>[^/]+)/?$', 'solaris.warbook.pilotskill.views.show_discipline')
)