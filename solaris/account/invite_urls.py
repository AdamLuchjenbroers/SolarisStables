from django.conf.urls import patterns, url

from . import views

app_name='invitations'
urlpatterns = patterns('',
    # These need to be in the invitations namespace so the django-invitations
    # module can derive the correct URLs
    url(r'^/?$', views.SolarisSendInvite.as_view(),
        name='send-invite'),
    url(r'^accept/(?P<key>\w+)/$', views.SolarisAcceptInvite.as_view(),
        name='accept-invite'),
)
