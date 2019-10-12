from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.CampaignToolsView.as_view(), name='campaign_tools_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.CampaignToolsView.as_view(), name='campaign_tools'),

    url(r'^mech-list/generate$', views.MechRollFormView.as_view(), name='campaign_tools_genmechlist'),
    url(r'^mech-list/?$', views.MechRollTableView.as_view(), name='campaign_tools_mechlist'),
]
