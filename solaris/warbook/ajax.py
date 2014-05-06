import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from solaris.views import SolarisView
from .models import House


class SolarisAjax(SolarisView):
    pass

class JsonHouseDisciplines(SolarisAjax):
        
    def get(self, request, house_name=''):
        house = get_object_or_404(House, house__iexact=house_name)
        
        house_disciplines = []        
        for discipline in house.house_disciplines.all():
            d = dict()
            d['id'] = discipline.id
            d['name'] = discipline.name 
            house_disciplines.append(d)
            
        return HttpResponse(json.dumps(house_disciplines))
            
        