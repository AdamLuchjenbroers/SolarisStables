from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect

from solaris.campaign.views import CampaignViewMixin, CampaignWeekMixin
from solaris.warbook.mech.views import MechSearchResultsView

from . import forms

class CampaignToolsView(CampaignWeekMixin, TemplateView):
    template_name = 'campaign/campaign_tools.html'
    view_url_name = 'campaign_tools'
    submenu_selected = 'Tools'

class MechRollTableView(MechSearchResultsView):
    template_name = 'campaign/campaign_mechlist.html'

    def get(self, request):
        return redirect('campaign_tools_genmechlist')

    def get_context_data(self, **kwargs):
        page_context = super(MechRollTableView, self).get_context_data(**kwargs)

class MechRollFormView(MechSearchResultsView):       
    template_name = 'campaign/forms/generate_mech_table.html'
    form_class = forms.MechRollListForm
    submenu_selected = 'Mechs'
    success_url='/reference/mechs/search'

    def get_context_data(self, **kwargs):
        page_context = super(MechRollFormView, self).get_context_data(**kwargs)
        page_context['submit'] = 'Search'
        page_context['post_url'] = '/reference/mechs/search'
        
        return page_context
