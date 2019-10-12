
from django.conf.urls import url, include

from . import views 

urlpatterns = [
    url(r'^$', views.StableOptionsView.as_view(), name='stable_options_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableOptionsView.as_view(), name='stable_options'),

    url(r'^(?P<week>[0-9]+)/set-logo$', views.StableSetLogoView.as_view(), name='stable_options_setlogo'),
    url(r'^(?P<week>[0-9]+)/set-banner$', views.StableSetBannerView.as_view(), name='stable_options_setbanner'),
]
