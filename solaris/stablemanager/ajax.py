import json

#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .views import StableWeekMixin
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.techtree.models import Technology

class StableWeekAjax(StableWeekMixin, View):
    def dispatch(self, request, *args, **kwargs):
        try: 
            return super(StableWeekAjax, self).dispatch(request, *args, **kwargs)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

    def get_call_parameter(self, request, name, urlparam):
	# Returns the call parameter, using the URL value if present
        # and falling back to POST or GET parameter values if it's
        # not.
        try:
            if urlparam != None:
                return urlparam
            elif request.method == 'POST':
                return request.POST[name]
            else:
                return request.GET[name]
        except KeyError:
            return None

class ProductionChassisAutocomplete(StableWeekAjax):
    def get(self, request):  
        chassis_list = {}

        if 'all' in request.GET and request.GET['all'] == 'T':
            source_set = MechDesign.objects.filter(production_type__in=('P','H'))
        else:        
            source_set = self.stableweek.supply_mechs
 
        for mech in source_set.filter(mech_name__icontains=request.GET['term']):
            chassis_list[mech.mech_name] = True

        return HttpResponse(json.dumps(chassis_list.keys())) 

class ListProductionVariants(StableWeekAjax):
    def get(self, request):
        variant_list = {}

        if 'all' in request.GET and request.GET['all'] == 'true':
            source_set = MechDesign.objects.filter(production_type__in=('P','H'))
        else:
            source_set = self.stableweek.supply_mechs
 
        for mech in source_set.filter(mech_name=request.GET['mech']):
            variant_list[mech.mech_code] = {
              'url' : mech.get_absolute_url()     
            , 'code' : mech.mech_code
            , 'omni' : mech.is_omni
            , 'loadout' : mech.omni_loadout
            , 'id' : mech.id
            }
            
            if mech.is_omni:
                variant_list[mech.mech_code]['name'] = '%s (%s)' % (mech.mech_code, mech.omni_loadout)
            else:
                variant_list[mech.mech_code]['name'] = mech.mech_code
                 
        return HttpResponse(json.dumps(variant_list)) 

class ListAvailableTechContracts(StableWeekAjax):
    def get(self, request, week=None):
        techlist = Technology.objects.exclude(id__in=self.stableweek.supply_contracts.all()).filter(name__icontains=request.GET['term'])
        technames = [ tech.name for tech in techlist ]

        return HttpResponse(json.dumps(technames)) 

class StableOverviewInfo(StableWeekAjax):
    def get(self, request, week=None):
        info = {
          'funds'      : '%i CBills' % self.stableweek.closing_balance()
        , 'prominence' : self.stableweek.prominence()
        , 'mechs'      : '%i (%i)' % (self.stableweek.mechs.count_nonsignature(), self.stableweek.mechs.count_all_available())
        , 'pilots'     : self.stableweek.pilots.count()
        }
        return HttpResponse(json.dumps(info)) 

