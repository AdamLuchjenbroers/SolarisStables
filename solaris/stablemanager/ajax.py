import json

#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .views import StableWeekMixin
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.techtree.models import Technology

class ProductionChassisAutocomplete(StableWeekMixin, View):
    def get(self, request):  
        chassis_list = {}

        source_set = self.stableweek.supply_mechs
        if 'all' in request.GET and request.GET['all'] == 'T':
            source_set = MechDesign.objects.filter(production_type__in=('P','H'))
        
        for mech in source_set.filter(mech_name__icontains=request.GET['term']):
            chassis_list[mech.mech_name] = True

        return HttpResponse(json.dumps(chassis_list.keys())) 

class ListProductionVariants(StableWeekMixin, View):
    def get(self, request):
        variant_list = {}

        source_set = self.stableweek.supply_mechs
        if 'all' in request.GET and request.GET['all'] == 'true':
            source_set = MechDesign.objects.filter(production_type__in=('P','H'))
        
        for mech in source_set.filter(mech_name=request.GET['mech']):
            variant_list[mech.mech_code] = mech.get_absolute_url()      
                 
        return HttpResponse(json.dumps(variant_list)) 

class ListAvailableTechContracts(StableWeekMixin, View):
    def get(self, request, week=None):
        techlist = Technology.objects.exclude(id__in=self.stableweek.supply_contracts.all()).filter(name__icontains=request.GET['term'])
        technames = [ tech.name for tech in techlist ]

        return HttpResponse(json.dumps(technames)) 
