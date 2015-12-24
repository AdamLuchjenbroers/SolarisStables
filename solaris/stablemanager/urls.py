from django.conf.urls import patterns, url

from .views import StableRegistrationView, StableOverview
from .ajax import ProductionChassisAutocomplete, ListProductionVariants


from solaris.stablemanager.ledger.views import StableLedgerView, StableLedgerDeleteView
from solaris.stablemanager.training.views import StableTrainingView
from solaris.stablemanager.actions.views import StableActionView
from solaris.stablemanager.pilots.views import StablePilotsView, StableNewPilotsView, InitialPilotNamingView
from solaris.stablemanager.mechs.views import InitialMechPurchaseView, StableMechsView
from solaris.stablemanager.repairs.views import CreateRepairBillView, RepairBillView, RepairBillLineView, AjaxCritObjectView

urlpatterns = patterns('',
    url(r'^/?$', StableOverview.as_view(), name='stable_overview'),
    url(r'^register/?$', StableRegistrationView.as_view(), name='stable_registration'),
    url(r'^initial-mechs/?$', InitialMechPurchaseView.as_view(), name='stable_initialmechs'),
    url(r'^initial-pilots/?$', InitialPilotNamingView.as_view(), name='stable_initialpilots'),

    url(r'^ledger/?$', StableLedgerView.as_view(), name='stable_ledger_now'),  
    url(r'^ledger/(?P<week>[0-9]+)/?$', StableLedgerView.as_view(), name='stable_ledger'),
    url(r'^ledger/delete/?$', StableLedgerDeleteView.as_view(), name='stable_ledger_delete'),

    url(r'^training/?$', StableTrainingView.as_view(), name='stable_training_now'),
    url(r'^training/(?P<week>[0-9]+)/?$', StableTrainingView.as_view(), name='stable_training'),

    url(r'^actions/?$', StableActionView.as_view()),
    url(r'^actions/(?P<week>[0-9]+)/?$', StableActionView.as_view()),

    url(r'^mechs/?$', StableMechsView.as_view()),

    url(r'^pilots/?$', StablePilotsView.as_view()),
    url(r'^add-pilot/?$', StableNewPilotsView.as_view(), name='pilots_add'),

    url(r'^mechs/repair/(?P<bill>[0-9]+)/?$', RepairBillView.as_view(), name='repair_bill'),
    url(r'^mechs/repair/new/(?P<stablemech>[0-9]+)/?$', CreateRepairBillView.as_view(), name='repair_bill_new'),
    url(r'^mechs/repair/(?P<bill>[0-9]+)/itemised', RepairBillLineView.as_view()),
    url(r'^mechs/repair/(?P<bill>[0-9]+)/setcrit', AjaxCritObjectView.as_view()),

    url(r'^query/list-produced/?$', ProductionChassisAutocomplete.as_view(), name = 'stable_query_mechauto'),    
    url(r'^query/list-variants/?$', ListProductionVariants.as_view(), name = 'stable_query_mechvariant') 
)
