from django.conf.urls import patterns, url, include

from . import views 

urlpatterns = patterns('',
    url(r'^/?$', views.StableLedgerView.as_view(), name='stable_ledger_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableLedgerView.as_view(), name='stable_ledger'),

    url(r'^(?P<week>[0-9]+)/add', views.AjaxAddLedgerForm.as_view(), name='stable_ledger_add'),

    url(r'^(?P<week>[0-9]+)/(?P<entry_id>[0-9]+)/set-cost', views.AjaxUpdateLedgerCostForm.as_view(), name='stable_ledger_set_cost'),
    url(r'^(?P<week>[0-9]+)/(?P<entry_id>[0-9]+)/set-description', views.AjaxUpdateLedgerDescriptionForm.as_view(), name='stable_ledger_set_description'),
    url(r'^(?P<week>[0-9]+)/(?P<entry_id>[0-9]+)/delete', views.AjaxRemoveLedgerItem.as_view(), name='stable_ledger_delete'),
)
