from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StablePilotsView.as_view(), name='stable_pilots_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StablePilotsView.as_view(), name='stable_pilots'),

    url(r'^/?add-pilot$', views.StableAddPilotFormView.as_view(), name='stable_add_pilot_now'),
    url(r'^/?(?P<week>[0-9]+)/+add-pilot?$', views.StableAddPilotFormView.as_view(), name='stable_add_pilot'),

    url(r'^/?(?P<callsign>[^/]+)/edit$', views.StableEditPilotFormView.as_view(), name='stable_edit_pilot_now'),
    url(r'^/?(?P<week>[0-9]+)/(?P<callsign>[^/]+)/edit$', views.StableEditPilotFormView.as_view(), name='stable_edit_pilot'),

    url(r'^/?pilot-list$', views.StablePilotsListPartView.as_view(), name="stable_pilot_list_now"),
    url(r'^/?(?P<week>[0-9]+)/+pilot-list$', views.StablePilotsListPartView.as_view(), name="stable_pilot_list"),

    url(r'^/?training$', views.StablePilotsTrainingPartView.as_view(), name="stable_training_now"),
    url(r'^/?(?P<week>[0-9]+)/+training$', views.StablePilotsTrainingPartView.as_view(), name="stable_training"),

    url(r'^/?trait$', views.StablePilotsTraitsPartView.as_view(), name="stable_trait_now"),
    url(r'^/?(?P<week>[0-9]+)/+trait$', views.StablePilotsTraitsPartView.as_view(), name="stable_trait"),

    url(r'^/?defer$', views.StablePilotsDeferredPartView.as_view(), name="stable_defer_now"),
    url(r'^/?(?P<week>[0-9]+)/+defer$', views.StablePilotsDeferredPartView.as_view(), name="stable_defer"),

    url(r'^/?set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp_now"),
    url(r'^/?(?P<week>[0-9]+)/+set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp"),

    url(r'^/?set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib_now"),
    url(r'^/?(?P<week>[0-9]+)/+set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib"),

    url(r'^/?training-opts', views.AjaxGetAvailableTraining.as_view(), name="stable_training_options_now"),
    url(r'^/?(?P<week>[0-9]+)/+training-opts', views.AjaxGetAvailableTraining.as_view(), name="stable_training_options"),

    url(r'^/?skill-list', views.AjaxGetPilotSkillsList.as_view(), name="stable_skill_list_now"),
    url(r'^/?(?P<week>[0-9]+)/+skill-list', views.AjaxGetPilotSkillsList.as_view(), name="stable_skill_list"),

    url(r'^/?add-training', views.AjaxAddPilotTraining.as_view(), name="stable_add_training_now"),
    url(r'^/?(?P<week>[0-9]+)/+add-training', views.AjaxAddPilotTraining.as_view(), name="stable_add_training"),

    url(r'^/?remove-training', views.AjaxRemovePilotTraining.as_view(), name="stable_remove_training_now"),
    url(r'^/?(?P<week>[0-9]+)/+remove-training', views.AjaxRemovePilotTraining.as_view(), name="stable_remove_training"),

    url(r'^/?add-trait', views.AjaxAddPilotTrait.as_view(), name="stable_add_trait_now"),
    url(r'^/?(?P<week>[0-9]+)/+add-trait', views.AjaxAddPilotTrait.as_view(), name="stable_add_trait"),

    url(r'^/?remove-trait', views.AjaxRemovePilotTrait.as_view(), name="stable_remove_trait_now"),
    url(r'^/?(?P<week>[0-9]+)/+remove-trait', views.AjaxRemovePilotTrait.as_view(), name="stable_remove_trait"),

    url(r'^/?cure-trait', views.AjaxCurePilotTrait.as_view(), name="stable_cure_trait_now"),
    url(r'^/?(?P<week>[0-9]+)/+cure-trait', views.AjaxCurePilotTrait.as_view(), name="stable_cure_trait"),

    url(r'^/?pilot-traits', views.AjaxGetCurrentPilotTraits.as_view(), name="stable_pilot_traits_now"),
    url(r'^/?(?P<week>[0-9]+)/+pilot-traits', views.AjaxGetCurrentPilotTraits.as_view(), name="stable_pilot_traits"),

    url(r'^/?add-deferred', views.AjaxAddPilotDeferred.as_view(), name="stable_add_deferred_now"),
    url(r'^/?(?P<week>[0-9]+)/+add-deferred', views.AjaxAddPilotDeferred.as_view(), name="stable_add_deferred"),

    url(r'^/?end-deferred', views.AjaxEndPilotDeferred.as_view(), name="stable_remove_deferred_now"),
    url(r'^/?(?P<week>[0-9]+)/+end-deferred', views.AjaxEndPilotDeferred.as_view(), name="stable_remove_deferred"),

    url(r'^/?set-status', views.AjaxSetPilotStatus.as_view(), name="stable_set_status_now"),
    url(r'^/?(?P<week>[0-9]+)/+set-status', views.AjaxSetPilotStatus.as_view(), name="stable_set_status"),
)
