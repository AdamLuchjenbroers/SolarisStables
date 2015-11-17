import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .views import StableWeekMixin

class ProductionChassisAutocomplete(StableWeekMixin, View):
    def get(self, request):
        print "[%s]" % request.GET['m']
        production = self.stable.house.produced_designs.filter(mech_name__icontains=request.GET['m'])
        
        equipment_list = self.stableweek.available_equipment()
  
        chassis_list = {}
        
        for mech in production.all():
            if mech.can_be_produced_with(equipment_list):
                chassis_list[mech.mech_name] = True

        return HttpResponse(json.dumps(chassis_list.keys())) 
