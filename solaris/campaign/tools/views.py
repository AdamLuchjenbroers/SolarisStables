from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from django.http import Http404

from random import shuffle

from solaris.utils import random_unique_set
from solaris.campaign.views import CampaignViewMixin, CampaignWeekMixin
from solaris.warbook.mech.views import MechSearchResultsView

from . import forms

tables = {
  '1D6'  : { 'items' : 6,  'grouping' : [''], 'per-group' : 6 }
, 'D6-2' : { 'items' : 12, 'grouping' : ['1-3', '4-6'], 'per-group' : 6 }
, 'D6-3' : { 'items' : 18, 'grouping' : ['1-2', '3-4', '5-6'], 'per-group' : 6 }
, '1D20' : { 'items' : 20, 'grouping' : [''], 'per-group' : 20 }
}

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

        tableinfo = tables[self.request.POST.get('table_type')]

        mech_list = self.get_queryset()
        mech_count = mech_list.count()
        to_get = tableinfo['items']
        
        if mech_count <= 0:
            raise Http404('No Mechs Found')

        fetch = range(mech_count) * (to_get / mech_count)
        fetch += random_unique_set(to_get % mech_count, 0, mech_count)
        shuffle(fetch)

        groups = []
            
        for label in tableinfo['grouping']:
            index_list =  [ fetch.pop() for i in range(tableinfo['per-group']) ]
            group_mechs = [ mech_list[idx] for idx in index_list ]

            groups.append((label, group_mechs))

        page_context['pergroup'] = tableinfo['per-group']
        page_context['groups'] = groups

        print groups

        return page_context;

class MechRollFormView(CampaignViewMixin, FormView):       
    template_name = 'campaign/forms/generate_mech_table.html'
    form_class = forms.MechRollListForm
    submenu_selected = 'Mechs'
    success_url='/reference/mechs/search'

    def get_context_data(self, **kwargs):
        page_context = super(MechRollFormView, self).get_context_data(**kwargs)
        page_context['submit'] = 'Search'
        page_context['post_url'] = '/reference/mechs/search'
        
        return page_context
