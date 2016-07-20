from django.conf.urls import patterns, include, url

from . import ajax, views

from solaris.stablemanager.training.views import StableTrainingView
from solaris.stablemanager.actions.views import StableActionView
from solaris.stablemanager.pilots.views import InitialPilotNamingView
from solaris.stablemanager.mechs.views import InitialMechPurchaseView

urlpatterns = patterns('',
    url(r'^/?$', views.StableOverview.as_view(), name='stable_overview_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableOverview.as_view(), name='stable_overview'),
    url(r'^create/?$', views.AjaxCreateStableWeekView.as_view(), name='stable_createweek'),

    url(r'^/?add-tech/?$', views.AjaxAddStableTech.as_view()),
    url(r'^(?P<week>[0-9]+)/add-tech/?$', views.AjaxAddStableTech.as_view()),

    url(r'^/?alter-rep/?$', views.AjaxAlterReputationView.as_view()),
    url(r'^(?P<week>[0-9]+)/alter-rep/?$', views.AjaxAlterReputationView.as_view()),

    url(r'^/?tech-list/?', views.StableTechListPart.as_view()),
    url(r'^(?P<week>[0-9]+)/tech-list/?', views.StableTechListPart.as_view()),

    url(r'^register/?$', views.StableRegistrationView.as_view(), name='stable_registration'),
    url(r'^initial-mechs/?$', InitialMechPurchaseView.as_view(), name='stable_initialmechs'),
    url(r'^initial-pilots/?$', InitialPilotNamingView.as_view(), name='stable_initialpilots'),

    url(r'^training/?$', StableTrainingView.as_view(), name='stable_training_now'),
    url(r'^training/(?P<week>[0-9]+)/?$', StableTrainingView.as_view(), name='stable_training'),

    url(r'^actions/?$', StableActionView.as_view(), name='stable_actions_now'),
    url(r'^actions/(?P<week>[0-9]+)/?$', StableActionView.as_view(), name='stable_actions'),

    url(r'^ledger/', include('solaris.stablemanager.ledger.urls')),
    url(r'^mechs/', include('solaris.stablemanager.mechs.urls')),
    url(r'^pilots/', include('solaris.stablemanager.pilots.urls')),

    url(r'^query/list-produced/?$', ajax.ProductionChassisAutocomplete.as_view(), name = 'stable_query_mechauto_now'), 
#    url(r'^(?P<week>[0-9]+)/list-produced/?$', ajax.ProductionChassisAutocomplete.as_view(), name = 'stable_query_mechauto'), 
   
    url(r'^query/list-variants/?$', ajax.ListProductionVariants.as_view(), name = 'stable_query_mechvariant_now'), 
#    url(r'^(?P<week>[0-9]+)/list-variants/?$', ajax.ListProductionVariants.as_view(), name = 'stable_query_mechvariant'),
 
    url(r'^/?list-techs/?$', ajax.ListAvailableTechContracts.as_view(), name = 'stable_query_availtechs_now'), 
    url(r'^(?P<week>[0-9]+)/list-techs/?$', ajax.ListAvailableTechContracts.as_view(), name = 'stable_query_availtechs'), 

    url(r'^/?overview/?$', ajax.StableOverviewInfo.as_view(), name = 'stable_query_overview_now'),
    url(r'^(?P<week>[0-9]+)/overview/?$', ajax.StableOverviewInfo.as_view(), name = 'stable_query_overview'),
)
