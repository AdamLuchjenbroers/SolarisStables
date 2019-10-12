from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^new-temp-mech$', views.CreateTempMechView.as_view(), name='files_upload_mech'),
]
