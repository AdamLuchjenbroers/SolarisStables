from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.views.generic import ListView, TemplateView, FormView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

from solaris.warbook.views import ReferenceViewMixin
from solaris.warbook.models import House
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.mech.forms import MechSearchForm
from solaris.stablemanager.models import Stable

class ReferenceMechMixin(ReferenceViewMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        try:
            self.stable = Stable.objects.get(owner=request.user)
        except Stable.DoesNotExist:
            self.stable = None
            
        return super(ReferenceMechMixin, self).dispatch(request, *args, **kwargs)

class MechDetailViewBase(ReferenceMechMixin, TemplateView):
    template_name = 'warbook/mechdetail.tmpl'
    filters = {}

    def get_context_data(self, **kwargs):
        page_context = super(MechDetailViewBase,self).get_context_data(**kwargs)
        
        page_context['mech'] = get_object_or_404(MechDesign
                                                , mech_name__iexact=self.kwargs['name']
                                                , mech_code__iexact=self.kwargs['code']
                                                , omni_loadout__iexact=self.kwargs.get('omni', 'Base')  
                                                , **self.__class__.filters)    
        page_context['detail_class'] = 'mech-view'
        page_context['required_techs'] = page_context['mech'].required_techs.all()
        if hasattr(self, 'stable'):
            page_context['stable_techs'] = self.stable.get_stableweek().supply_contracts.all()
        
        return page_context

class MechDetailView(MechDetailViewBase):
    filters = {'production_type__in' : ('P', 'H') }
    submenu_selected = 'Mechs'

class CustomMechDetailView(MechDetailViewBase):
    filters = {'production_type' : 'C' }
    submenu_selected = 'Mechs'

class MechListView(ReferenceMechMixin, ListView):
    template_name = 'warbook/mechlist.tmpl'
    model = MechDesign
    submenu_selected = 'Mechs'
    
    def get_queryset(self):
        return get_list_or_404(MechDesign, mech_name__iexact=self.kwargs['name'], production_type='P', omni_loadout__iexact='Base')
    
    def get_context_data(self):
        page_context = super(MechListView, self).get_context_data()
        
        page_context['chassis'] = self.kwargs['name']
        return page_context

class MechSearchResultsView(ReferenceMechMixin, ListView):
    template_name = 'warbook/mechlist.tmpl'
    model = MechDesign
    submenu_selected = 'Mechs'
    
    translate_terms = {
        u'mech_name' : 'mech_name__iexact',
        u'mech_code' : 'mech_code__iexact',
        u'tonnage_low' : 'tonnage__gte',
        u'tonnage_high' : 'tonnage__lte',
        u'cost_low' : 'credit_value__gte',
        u'cost_high' : 'credit_value__lte',
        u'bv_low' : 'bv_value__gte',
        u'bv_high' : 'bv_value__lte',
        u'tier_low' : 'tier__gte',
        u'tier_high' : 'tier__lte',
    }
    
    def get_filter_args(self, requestdata):
        filter_args = {'production_type' : 'P', 'omni_loadout__iexact' : 'Base'}
        
        for (term, query_term) in MechSearchResultsView.translate_terms.items() :
            if term in requestdata and requestdata[term] != '':
                filter_args[query_term] = requestdata[term]

        if requestdata['available_to'] == '-':
            self.allmechs = MechDesign.objects.all()
        elif requestdata['available_to'] == 'me':
            self.allmechs = self.stable.get_stableweek().supply_mechs.all()
        else:
            # It's a house name, so get the house list for filtering
            house = get_object_or_404( House, id=requestdata['available_to'])
            self.allmechs = house.produced_designs.all()                     
  
        return filter_args
        
    def post(self, request):
            if request.POST:
                self.filter_args = self.get_filter_args(request.POST)
                return super(MechSearchResultsView, self).get(request)
            else:
                return redirect('/reference/mechs')
         
    def get(self, request):
        if request.GET:
            self.filter_args = self.get_filter_args(request.GET)
            return super(MechSearchResultsView, self).get(request)
        else:
            return redirect('/reference/mechs')
        
    def get_queryset(self):
        return self.allmechs.filter(**self.filter_args) 
    
    def get_context_data(self):
        page_context = super(MechSearchResultsView, self).get_context_data()
        
        page_context['chassis'] = 'Search Results'
        return page_context
         
class MechSearchView(ReferenceMechMixin, FormView):       
    template_name = 'warbook/mechsearch.tmpl'
    form_class = MechSearchForm
    submenu_selected = 'Mechs'
    success_url='/reference/mechs/search'

    def get_context_data(self, **kwargs):
        page_context = super(MechSearchView, self).get_context_data(**kwargs)

        page_context['submit'] = 'Search'
        page_context['post_url'] = '/reference/mechs/search'
        
        return page_context
        
