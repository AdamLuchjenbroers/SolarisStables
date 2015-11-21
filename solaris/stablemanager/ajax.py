import json

#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .views import StableWeekMixin

class ProductionChassisAutocomplete(StableWeekMixin, View):
    def get(self, request):  
        chassis_list = {}
        
        for mech in self.stableweek.supply_mechs.filter(mech_name__icontains=request.GET['term']):
            chassis_list[mech.mech_name] = True

        return HttpResponse(json.dumps(chassis_list.keys())) 

class ListProductionVariants(StableWeekMixin, View):
    def get(self, request):
        variant_list = {}
        
        for mech in self.stableweek.supply_mechs.filter(mech_name=request.GET['mech']):
            variant_list[mech.mech_code] = True      
                 
        return HttpResponse(json.dumps(variant_list.keys()))  