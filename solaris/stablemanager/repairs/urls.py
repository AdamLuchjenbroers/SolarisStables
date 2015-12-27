from django.conf.urls import patterns, url

from solaris.stablemanager.repairs import views 

urlpatterns = patterns('',
    url(r'^(?P<bill>[0-9]+)/?$', views.RepairBillView.as_view(), name='repair_bill'),
    url(r'^new/(?P<stablemech>[0-9]+)/?$', views.CreateRepairBillView.as_view(), name='repair_bill_new'),
    url(r'^(?P<bill>[0-9]+)/itemised', views.RepairBillLineView.as_view()),
    url(r'^(?P<bill>[0-9]+)/setcrit', views.AjaxCritObjectView.as_view()),
    url(r'^(?P<bill>[0-9]+)/setdamage', views.AjaxDamageLocationView.as_view()),
    url(r'^(?P<bill>[0-9]+)/destroy', views.AjaxDestroyLocationView.as_view()),
)
