from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.views.generic import ListView, TemplateView, FormView

from solaris.warbook.views import ReferenceViewMixin
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.mech.forms import MechSearchForm

class MechDetailView(ReferenceViewMixin, TemplateView):
    template_name = 'warbook/mechdetail.tmpl'
    model = MechDesign
    submenu_selected = 'Mechs'
    
    def get_context_data(self, **kwargs):
        page_context = super(MechDetailView,self).get_context_data(**kwargs)

        if not('omni' in self.kwargs.keys()):
            self.kwargs['omni'] = 'Base'
        
        page_context['mech'] = get_object_or_404(MechDesign
                                                , mech_name__iexact=self.kwargs['name']
                                                , mech_code__iexact=self.kwargs['code']
                                                , omni_loadout__iexact=self.kwargs['omni']  
                                                , production_type='P')
        page_context['crit_table'] = { location.location_code() : location for location in page_context['mech'].locations.all() }
        
        return page_context

class MechListView(ReferenceViewMixin, ListView):
    template_name = 'warbook/mechlist.tmpl'
    model = MechDesign
    submenu_selected = 'Mechs'
    
    def get_queryset(self):
        return get_list_or_404(MechDesign, mech_name__iexact=self.kwargs['name'], production_type='P', omni_loadout__iexact='Base')
    
    def get_context_data(self):
        page_context = super(MechListView, self).get_context_data()
        
        page_context['chassis'] = self.kwargs['name']
        return page_context

class MechSearchResultsView(ReferenceViewMixin, ListView):
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
    }
    
    def get_filter_args(self, requestdata):
        filter_args = {'production_type' : 'P', 'omni_loadout__iexact' : 'Base'}
        
        for (term, query_term) in MechSearchResultsView.translate_terms.items() :
            if term in requestdata and requestdata[term] != '':
                filter_args[query_term] = requestdata[term]

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
        return get_list_or_404(MechDesign, **self.filter_args)
    
    def get_context_data(self):
        page_context = super(MechSearchResultsView, self).get_context_data()
        
        page_context['chassis'] = 'Search Results'
        return page_context
         
class MechSearchView(ReferenceViewMixin, FormView):       
    template_name = 'solaris_basicform.tmpl'
    form_class = MechSearchForm
    submenu_selected = 'Mechs'

    def get_context_data(self, **kwargs):
        page_context = super(MechSearchView, self).get_context_data(**kwargs)

        page_context['submit'] = 'Search'
        return page_context
        
