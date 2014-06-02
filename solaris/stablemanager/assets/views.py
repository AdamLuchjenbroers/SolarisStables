from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from solaris.warbook.pilotskill.models import PilotRank
from solaris.stablemanager.views import StableViewMixin, StableWeekMixin

from . import forms

class StablePilotsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/stable_pilots.tmpl'

class StableNewPilotsView(StableViewMixin, TemplateView):
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
        ,   'week' : self.stable.current_week
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
            return redirect('/')
        
        return self.get(request)

    def form_valid(self, form):        
        self.object = form.save(commit=False)
        
        if self.form_pilotweek.is_valid():
            self.form_skillset.instance = self.form_pilotweek.instance
            if self.form_skillset.is_valid():
                self.form_pilot.save()
                self.form_pilotweek.save()
                self.form_skillset.save()
