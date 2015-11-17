import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .models import House


class AjaxView(View):
    pass

class JsonHouseDisciplines(AjaxView):
    def get(self, request, house_name=''):
        house = get_object_or_404(House, house__iexact=house_name)
        
        house_disciplines = []
        house_disciplines.append({'choose-limit': 2})
        
        for discipline in house.house_disciplines.all():
            d = dict()
            d['id'] = discipline.id
            d['name'] = discipline.name 
            house_disciplines.append(d)
            
        return HttpResponse(json.dumps(house_disciplines))
            
        
