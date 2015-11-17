import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .views import StableWeekMixin
from .models import StableWeek

class ProductionChassisAutocomplete(StableWeekMixin, View):
    def get(self, request):
        production = self.stable.house.produced_designs.filter(mech_name__icontains=request.GET['m'])
  
        chassis_list = {}
        
        for mech in production.all():
            # TODO: Check available equipment
            chassis_list[mech.mech_name] = True

        return HttpResponse(json.dumps(chassis_list.keys())) 
