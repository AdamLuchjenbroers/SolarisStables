from django.conf.urls import patterns

from .views import StableRegistrationView, StableOverview
from solaris.stablemanager.ledger.views import StableLedgerView
from solaris.stablemanager.training.views import StableTrainingView
from solaris.stablemanager.actions.views import StableActionView

urlpatterns = patterns('',
    (r'^/?$', StableOverview.as_view()),
    (r'^register/?$', StableRegistrationView.as_view()),
    (r'^ledger/?$', StableLedgerView.as_view()),  
    (r'^ledger/(?P<week>[0-9]+)/?$', StableLedgerView.as_view()),
    (r'^training/?$', StableTrainingView.as_view()),
    (r'^training/(?P<week>[0-9]+)/?$', StableTrainingView.as_view()),
    (r'^actions/?$', StableActionView.as_view()),
    (r'^actions/(?P<week>[0-9]+)/?$', StableActionView.as_view()),
    
)