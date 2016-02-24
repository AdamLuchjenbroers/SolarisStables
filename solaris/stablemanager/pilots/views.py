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
                value = max(0,min(value,6))
                pilotweek.wounds = value
            else:
                return HttpResponse('Unrecognised Attribute: %s' % attribute, status=400)

            pilotweek.save()

            result = {
              'callsign' : pilot.pilot_callsign
            , 'value'    : value
            , 'total-cp' : pilotweek.character_points()
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


class StableNewPilotsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/forms/form_pilots.tmpl'

    def create_forms(self, pilot=None):
        if hasattr(self, 'form_pilot'):
            #Already done
            return
        
        pilot_initial = {
            'stable' : self.stable.id
        ,   'affiliation' : self.stable.house.id
        }
        pilotweek_initial = {
            'pilot_rank' : PilotRank.objects.get(rank='Rookie')
        ,   'skill_gunnery' : 5
        ,   'skill_pilotting' : 6
        ,   'start_character_points' : 0
        ,   'week' : self.stableweek
        }        
                
        if pilot:
            pilotweek_initial['pilot'] = pilot
        
        if self.request.POST:
            self.form_pilot = forms.PilotForm(self.request.POST, initial=pilot_initial, instance=pilot)
            self.form_pilotweek = forms.PilotWeekForm(self.request.POST, initial=pilotweek_initial)
            self.form_skillset = forms.PilotInlineSkillsForm(self.request.POST)
        else:
            self.form_pilot = forms.PilotForm(initial=pilot_initial, instance=pilot)
            self.form_pilotweek = forms.PilotWeekForm(initial=pilotweek_initial)
            self.form_skillset = forms.PilotInlineSkillsForm()
        return self.form_pilot, self.form_pilotweek, self.form_skillset 
   
    def get_context_data(self, **kwargs):
        page_context = super(StableNewPilotsView, self).get_context_data(**kwargs)
        
        page_context['pilot'] = self.form_pilot
        page_context['pilotweek'] = self.form_pilotweek
        page_context['skillset'] = self.form_skillset
        
        page_context['post_url'] = reverse('pilots_add')
        page_context['submit'] = 'Add'
        page_context['form_class'] = 'pilot'
        
        return page_context
    
    def get(self, request):
        self.create_forms()
        return super(StableNewPilotsView, self).get(request)
    
    def post(self, request):
        self.create_forms()
        self.form_pilot.fields['stable'].value = self.stable
        
        v_pilot = self.form_pilot.is_valid()
        v_pilotweek = self.form_pilotweek.is_valid()
        v_skillset = self.form_skillset.is_valid()
        if v_pilot and v_pilotweek and v_skillset:
            pilot = self.form_pilot.save(commit=False)
            pilot.stable = self.stable
            pilot.save()
            
            pilotweek = self.form_pilotweek.save(commit=False)
            pilotweek.week = self.stable.current_week
            pilotweek.pilot = pilot
            pilotweek.save()

            self.form_skillset.instance = pilotweek
            self.form_skillset.save()
            return redirect(reverse('stable_overview'))
        else: 
            return self.get(request)

    def form_valid(self, form):        
        self.object = form.save(commit=False)
        
        if self.form_pilotweek.is_valid():
            self.form_skillset.instance = self.form_pilotweek.instance
            if self.form_skillset.is_valid():
                self.form_pilot.save()
                self.form_pilotweek.save()
                self.form_skillset.save()
