from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StablePilotsView.as_view(), name='stable_pilots_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StablePilotsView.as_view(), name='stable_pilots'),

    url(r'^set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp_now"),
    url(r'^(?P<week>[0-9]+)/set-tp', views.AjaxSetTrainingPoints.as_view(), name="stable_set_tp"),

    url(r'^set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib_now"),
    url(r'^(?P<week>[0-9]+)/set-attrib', views.AjaxSetPilotAttribute.as_view(), name="stable_set_attrib"),

    url(r'^add?$', views.StableNewPilotsView.as_view(), name='pilots_add'),
)
