from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^techtree$', 'solaris.cms.views.util_redirect', {'path': '/reference/techtree/'}),
    (r'^techtree/$',  'solaris.warbook.techtree.views.list_technologies', {'selected': '/techtree/'}),
    (r'^techtree/(?P<technology>[^/]+)/$', 'solaris.warbook.techtree.views.display_technology', {'selected': '/techtree/'}),
    (r'^pilotskills/$', 'solaris.warbook.pilotskill.views.list_disciplines')
)