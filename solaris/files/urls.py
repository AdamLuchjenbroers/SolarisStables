from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^new-temp-mech?$', views.CreateTempMechView.as_view(), name='files_upload_mech'),
)