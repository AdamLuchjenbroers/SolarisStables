from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StablePilotsView.as_view(), name='stable_pilots_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StablePilotsView.as_view(), name='stable_pilots'),

    url(r'^set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp_now"),
    url(r'^(?P<week>[0-9]+)/set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp"),

    url(r'^set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib_now"),
    url(r'^(?P<week>[0-9]+)/set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib"),

    url(r'^training-opts', views.AjaxGetAvailableTraining.as_view(), name="stable_training_options_now"),
    url(r'^(?P<week>[0-9]+)/training-opts', views.AjaxGetAvailableTraining.as_view(), name="stable_training_options"),

    url(r'^skill-list', views.AjaxGetPilotSkillsList.as_view(), name="stable_skill_list_now"),
    url(r'^(?P<week>[0-9]+)/skill-list', views.AjaxGetPilotSkillsList.as_view(), name="stable_skill_list"),

    url(r'^add-training', views.AjaxAddPilotTraining.as_view(), name="stable_add_training_now"),
    url(r'^(?P<week>[0-9]+)/add-training', views.AjaxAddPilotTraining.as_view(), name="stable_add_training"),
)
