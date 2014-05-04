#from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from solaris.warbook.views import ReferenceView
from solaris.warbook.mech.models import MechDesign

class MechDetailView(ReferenceView):
    def get(self, request, name='', code=''):
        
        mech = get_object_or_404(MechDesign, mech_name=name, mech_code=code)        
        
        tmpl_mech = loader.get_template('warbook/mechs/mech_detail.tmpl')    
        body = Markup(tmpl_mech.generate(mech=mech))
        body = Markup('<p>Detail page for %s %s</p>' % (name, code))
        return HttpResponse(self.in_layout(body, request))


class MechListView(ReferenceView):
    def get(self, request, name=''):
        body = Markup('<p>List of all %s variants to go here</p>' % name)
        
        return HttpResponse(self.in_layout(body, request))
        

class MechSearchView(ReferenceView):
    def get(self, request):
        body = Markup('<p>Search form for Mech Database to go here</p>')
        
        return HttpResponse(self.in_layout(body, request))
        