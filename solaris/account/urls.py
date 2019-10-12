from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^email-sent/$', views.SolarisRegistrationEmailSentView.as_view(),
        name='account_email_verification_sent'),
    url(r"^confirm-email/(?P<key>[^/]+)/$", views.SolarisConfirmEmailView.as_view(),
        name="account_confirm_email"),

    # Duplicated here as a secondary option                   
    url(r'^login/?$', views.SolarisLoginView.as_view()),

    url(r'^reset-password/$', views.SolarisPasswordResetView.as_view(),
        name='account_reset_password'),
    url(r"^reset-done/$", views.SolarisPasswordResetDoneView.as_view(),
        name="account_reset_password_done"),
    url(r"^reset-password/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.SolarisPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^reset-password/key/done/$", views.SolarisPasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),

    url(r'^register/?$', views.SolarisRegistrationView.as_view()), 
]
