import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from urllib import unquote

from .models import House
from .mech.models import MechDesign


class AjaxView(View):
    pass

class JsonHouseDisciplines(AjaxView):
    def get(self, request, house_name=''):
        house = get_object_or_404(House, house__iexact=house_name)
        
        house_disciplines = []
        house_disciplines.append({'choose-limit': house.selectable_disciplines})
        
        for discipline in house.house_disciplines.all():
            d = dict()
            d['id'] = discipline.id
            d['name'] = discipline.name 
            house_disciplines.append(d)
            
        return HttpResponse(json.dumps(house_disciplines))

class JsonMechInformationView(AjaxView):
    def dispatch(self, request, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse(status=403)
        
        try:
            mech_name = unquote(request.GET['chassis'])
            mech_code = unquote(request.GET['type'])
            self.mech = get_object_or_404(MechDesign, mech_name=mech_name, mech_code=mech_code)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 401)
        
        return super(JsonMechInformationView, self).dispatch(request, **kwargs)
        
            
class JsonPriceOfMech(JsonMechInformationView): 
    def get(self, request):         
        return HttpResponse(json.dumps(self.mech.credit_value))
            
class JsonBattleValueOfMech(JsonMechInformationView): 
    def get(self, request):         
        return HttpResponse(json.dumps(self.mech.bv_value))
