from django.views.generic import View, TemplateView, ListView, FormView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse 

import json
from urllib import unquote

from solaris.warbook.pilotskill.models import PilotRank
from solaris.stablemanager.views import StableViewMixin, StableWeekMixin

from . import forms, models

class StablePilotsView(StableWeekMixin, ListView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/stable_pilots.tmpl'
    model = models.PilotWeek    
    view_url_name = 'stable_pilots'

    def get_queryset(self):
        return models.PilotWeek.objects.filter(week=self.stableweek)

    def get_context_data(self, **kwargs):
        page_context = super(StablePilotsView, self).get_context_data(**kwargs)

        available_disciplines = self.stable.stable_disciplines.all() | self.stable.house.house_disciplines.all()
        page_context['available_disciplines'] = available_disciplines.distinct().order_by('name')

        page_context['training_form'] = forms.PilotTrainingForm(stableweek=self.stableweek)

        return page_context
        
class InitialPilotNamingView(StableViewMixin, FormView):
    template_name = 'stablemanager/initial_pilots.tmpl'
    form_class = forms.PilotNamingFormSet
    success_url = '/stable'

    def get_form_kwargs(self):
        kwargs = super(InitialPilotNamingView, self).get_form_kwargs()
        if self.request.method == 'GET':
            kwargs['queryset'] = self.stable.pilots.filter(pilot_callsign__startswith='Unnamed')

        return kwargs

    def form_valid(self, form):
        for pilot in form:
            pilot.instance.save()

        return super(InitialPilotNamingView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        page_context = super(InitialPilotNamingView, self).get_context_data(**kwargs)
        
        page_context['submit'] = 'Rename All'
        return page_context
        
class AjaxSetTrainingPoints(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            self.stableweek.training_points = int(request.POST['training-points'])
            self.stableweek.save()

            result = {
              'rookie-tp'    : self.stableweek.rookie_tp()
            , 'contender-tp' : self.stableweek.contender_tp()
            , 'total-tp'     : self.stableweek.training_points
            }

            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

class AjaxSetPilotAttribute(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            pilot = models.Pilot.objects.get(pilot_callsign=unquote(request.POST['callsign']), stable=self.stable)
            pilotweek = models.PilotWeek.objects.get(pilot=pilot, week=self.stableweek)

            attribute = request.POST['attribute']
            value = int(request.POST['value']) 
            if attribute == 'cp':
                pilotweek.adjust_character_points = value
            elif attribute == 'tp':
                pilotweek.assigned_training_points = value
            elif attribute == 'wounds':
                value = pilotweek.set_wounds(value)
            elif attribute == 'fame':
                value = pilotweek.set_fame(value)
            else:
                return HttpResponse('Unrecognised Attribute: %s' % attribute, status=400)

            pilotweek.save()

            result = {
              'callsign' : pilot.pilot_callsign
            , 'value'    : value
            , 'total-cp' : pilotweek.character_points()
            , 'is-dead'  : pilotweek.is_dead()
            , 'tp-table' : pilotweek.week.assigned_tp_counts()
            }

            return HttpResponse(json.dumps(result))
  
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)
        except models.Pilot.DoesNotExist:
            return HttpResponse('Unrecognised Callsign', status=404)
        except models.PilotWeek.DoesNotExist:
            return HttpResponse('Cannot find Pilot Week', status=404)
