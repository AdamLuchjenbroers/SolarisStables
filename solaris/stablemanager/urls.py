from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^/?$', 'solaris.stablemanager.views.stable_main'),
    (r'^register/?$', 'solaris.stablemanager.views.stable_registration', ),
)