#from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView


from solaris.utils import deepcopy_append
from solaris.views import PageObject, SolarisViewMixin
from solaris.warbook.views import ReferenceView
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.mech.forms import MechSearchForm

class MechView(ReferenceView):
    submenu_selected = 'Mechs'

class MechCritTable(PageObject):
    template = 'warbook/mechs/mech_crittable.genshi'

class MechDetailView(MechView):
    styles_list = deepcopy_append(MechView.styles_list, ['/static/css/mech_detail.css'])
    
    def __init__(self, *args, **kwargs):
        self.template = loader.get_template('warbook/mechs/mech_detail.genshi')
        super(MechDetailView, self).__init__(*args, **kwargs) 
    
    def get(self, request, name='', code=''):        
        mech_model = get_object_or_404(MechDesign, mech_name__iexact=name, mech_code__iexact=code)
                
        crit_tables = dict()
        for location in mech_model.locations.all():
            if location.structure:
                crit_tables[location.location_code()] = MechCritTable(location=location)
        
        crit_rows = (
            ['HD']
        ,   ['LA','LT','CT','RT','RA']
        ,   ['LL','LFL','LRL','RL','RFL', 'RLL']
        )
        
        body = Markup( self.template.generate(mech=mech_model, crit_tables=crit_tables, crit_rows=crit_rows))
        return HttpResponse(self.in_layout(body, request))

class MechListView(SolarisViewMixin, ListView):
    template_name = 'warbook/mechlist.tmpl'
    model = MechDesign
    
    def get_queryset(self):
        return get_list_or_404(MechDesign, mech_name__iexact=self.kwargs['name'])
    
    def get_context_data(self):
        page_context = super(MechListView, self).get_context_data()
        
        page_context['chassis'] = self.kwargs['name']
        return page_context

class MechSearchResultsView(MechView):
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
    
    def search(self, fields):
        search = dict()
        
        print fields['tonnage_low']
        for (term, qterm) in MechSearchResultsView.translate_terms.items() :
            if term in fields and fields[term] != '':
                print '  %s: %s' % (qterm, fields[term])
                search[qterm] = fields[term]
        print search
        
        return get_list_or_404(MechDesign, **search)
    
    def post(self, request):
        tmpl_mech = loader.get_template('warbook/mechs/mech_listing.genshi')
        
        mech_list = self.search(request.POST)
        body = Markup(tmpl_mech.generate(mech_name='Search Results', mech_list=mech_list))
        
        return HttpResponse(self.in_layout(body, request))
    
    def get(self, request):
        return redirect('/reference/mechs')
            

class MechSearchView(ReferenceView):
    def get(self, request):
        form = MechSearchForm()
        
        search_form = loader.get_template('solaris_form_outer.genshi')
        body = Markup(search_form.generate(form_items=Markup(form.as_p()), formclass='mechsearch', post_url='/reference/mechs/search/', submit='Search')) 
        
        return HttpResponse(self.in_layout(body, request))
        
