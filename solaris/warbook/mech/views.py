#from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse

from solaris.warbook.views import ReferenceView
from solaris.warbook.mech.models import MechDesign

class MechDetailView(ReferenceView):
    def get(self, request, name='', code=''):        
        mech = get_object_or_404(MechDesign, mech_name__iexact=name, mech_code__iexact=code)
        
        tmpl_mech = loader.get_template('warbook/mechs/mech_detail.tmpl')
        body = Markup(tmpl_mech.generate(mech=mech))
        return HttpResponse(self.in_layout(body, request))


class MechListView(ReferenceView):
    def get(self, request, name=''):
        mech_list = get_list_or_404(MechDesign, mech_name__iexact=name)
        
        tmpl_mech = loader.get_template('warbook/mechs/mech_listing.tmpl')
        body = Markup(tmpl_mech.generate(mech_name=name.title(), mech_list=mech_list))
        
        return HttpResponse(self.in_layout(body, request))


class MechSearchResultsView(ReferenceView):
    translate_terms = {
        'mech_name' : 'mech_name__iexact',
        'mech_code' : 'mech_code__iexact',
        'tonnage_low' : 'tonnage__gte',
        'tonnage_high' : 'tonnage__lte',
        'cost_low' : 'credit_value__gte',
        'cost_high' : 'credit_value__lte',
        'bv_low' : 'bv_value__gte',
        'bv_high' : 'bv_value__lte',
    }
    
    def search(self, fields):
        search = dict()
        for (term, qterm) in MechSearchResultsView.translate_terms:
            if term in fields[term] and fields[term] != None:
                search[qterm] = fields[term]
        
        return get_list_or_404(MechDesign, **search)
    
    def post(self, request):
        tmpl_mech = loader.get_template('warbook/mechs/mech_listing.tmpl')
        
        mech_list = self.search(request.POST)
        body = Markup(tmpl_mech.generate(mech_name='Search Results', mech_list=mech_list))
        
        return HttpResponse(self.in_layout(body, request))
    
    def get(self, request):
        return redirect('/reference/mechs')
            

class MechSearchView(ReferenceView):
    def get(self, request):
        body = Markup('<p>Search form for Mech Database to go here</p>')
        
        return HttpResponse(self.in_layout(body, request))
        