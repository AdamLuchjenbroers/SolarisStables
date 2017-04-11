from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StableActionView.as_view(), name='stable_actions_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableActionView.as_view(), name='stable_actions'),

    url(r'^(?P<week>[0-9]+)/list$', views.StableActionListPart.as_view(), name='stable_actions_list'),
    url(r'^(?P<week>[0-9]+)/management$', views.StableManagementPart.as_view(), name='stable_actions_management'),

    url(r'^(?P<week>[0-9]+)/add$', views.StableActionFormView.as_view(), name='stable_add_action'),
    url(r'^(?P<week>[0-9]+)/start-week$', views.AjaxSetWeekStarted.as_view(), name='stable_start_week'),

    url(r'^(?P<week>[0-9]+)/(?P<pk>[0-9]+)/delete$', views.AjaxRemoveAction.as_view(), name='stable_delete_action'),
    url(r'^(?P<week>[0-9]+)/(?P<pk>[0-9]+)/set-notes$', views.AjaxSetActionNotes.as_view(), name='stable_action_set_notes'),
    url(r'^(?P<week>[0-9]+)/(?P<pk>[0-9]+)/set-cost$', views.AjaxSetActionCost.as_view(), name='stable_action_set_cost'),
)
