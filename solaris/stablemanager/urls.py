from django.conf.urls import patterns

from solaris.stablemanager.views import StableRegistrationView

urlpatterns = patterns('',
    (r'^/?$', 'solaris.stablemanager.views.stable_main'),
    (r'^register/?$', StableRegistrationView.as_view()),
)