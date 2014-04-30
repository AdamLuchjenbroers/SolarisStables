from django.conf.urls import patterns

from solaris.stablemanager.views import StableRegistrationView, StableOverview

urlpatterns = patterns('',
    (r'^/?$', StableOverview.as_view()),
    (r'^register/?$', StableRegistrationView.as_view()),
)