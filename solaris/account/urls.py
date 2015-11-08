from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    url(r'^confirm-email/$', views.SolarisConfirmEmailView.as_view(),
        name='confirm_email'),
    # Duplicated here as a secondary option                   
    url(r'^login/?$', views.SolarisLoginView.as_view()),

    url(r'^reset-password/$', views.SolarisPasswordResetView.as_view(),
        name='account_reset_password'),
    url(r"^reset-password/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.SolarisPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
                                             
    # These need to be in the invitations namespace so the django-invitations
    # module can derive the correct URLs
    url(r'^invite/$', views.SolarisSendInvite.as_view(),
        name='send-invite'),
    url(r'^accept-invite/(?P<key>\w+)/$', views.SolarisAcceptInvite.as_view(),
        name='accept-invite'),
)
