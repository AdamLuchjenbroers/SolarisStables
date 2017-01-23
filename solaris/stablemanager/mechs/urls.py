from django.conf.urls import patterns, url, include

from . import views, pdf 

urlpatterns = patterns('',
    url(r'^/?$', views.StableMechsView.as_view(), name='stable_mechs_now'),
    url(r'^(?P<week>[0-9]+)/?$', views.StableMechsView.as_view(), name='stable_mechs'),

    url(r'^(?P<week>[0-9]+)/list/?$', views.StableMechsListPart.as_view()),
    url(r'^/?list/?$', views.StableMechsListPart.as_view()),

    url(r'^(?P<week>[0-9]+)/purchase/?$', views.MechPurchaseFormView.as_view()),
    url(r'^/?purchase/?$', views.MechPurchaseFormView.as_view()),

    url(r'^refit/(?P<smw_id>[0-9]+)/?$', views.MechRefitFormView.as_view(), name='refit_mech'),
    url(r'^refit/(?P<smw_id>[0-9]+)/upload$', views.RefitUploadMechView.as_view(), name='upload_refit_mech'),

    url(r'^loadouts/(?P<smw_id>[0-9]+)/?$', views.MechLoadoutsFormView.as_view(), name='loadout_mech'),
    url(r'^loadouts/(?P<smw_id>[0-9]+)/upload$', views.OmniUploadMechView.as_view(), name='upload_loadout_mech'),
    url(r'^loadouts/(?P<smw_id>[0-9]+)/remove$', views.MechRemoveConfigView.as_view(), name='remove_loadout'),

    url(r'^remove/(?P<smw_id>[0-9]+)/?$', views.MechRemoveAjaxView.as_view(), name='remove_mech'),
    url(r'^edit/(?P<smw_id>[0-9]+)/?$', views.MechEditFormView.as_view(), name='edit_mech'),

    url(r'^upload/purchase$', views.PurchaseUploadMechView.as_view(), name='upload_purchase_mech'),

    url(r'^pdf/?$', pdf.MechListPDFView.as_view(), name='stable_mechs_pdf_now'),
    url(r'^pdf/(?P<week>[0-9]+)/?$', pdf.MechListPDFView.as_view(), name='stable_mechs_pdf'),

    url(r'^repair/', include('solaris.stablemanager.repairs.urls')),
)
