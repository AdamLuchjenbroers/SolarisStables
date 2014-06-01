from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from solaris.warbook.pilotskill.models import PilotRank
from solaris.stablemanager.views import StableViewMixin, StableWeekMixin

from . import forms

class StablePilotsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/stable_pilots.tmpl'

class StableNewPilotsView(StableViewMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/forms/form_pilots.tmpl'
    success_url = reverse ('pilots_add')

    def create_additional_forms(self, pilot=None):
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
            pilotweek = forms.PilotWeekForm(self.request.POST, initial=pilotweek_initial)
            skillset = forms.PilotInlineSkillsForm(self.request.POST)
        else:
            pilotweek = forms.PilotWeekForm(initial=pilotweek_initial)
            skillset = forms.PilotInlineSkillsForm()
        return pilotweek, skillset 
            
    def get_initial(self):
        return {
            'stable' : self.stable
        }
   
    def get_context_data(self, **kwargs):
        page_context = super(StableNewPilotsView, self).get_context_data(**kwargs)
        
        page_context['pilot'] = forms.PilotForm(initial={
            'stable' : self.stable.id
        ,   'affiliation' : self.stable.house.id
        })
        
        ( page_context['pilotweek'], page_context['skillset']) = self.create_additional_forms()
        
        page_context['post_url'] = reverse ('pilots_add')
        page_context['submit'] = 'Add'
        page_context['form_class'] = 'pilot'
        
        return page_context
    
    def form_valid(self, form):        
        self.object = form.save(commit=False)
        
        (pilotweek, skillset) = self.create_additional_forms(pilot=self.object)
        if pilotweek.is_valid():
            skillset.instance = pilotweek.instance
            if skillset.isv_valid():
                form.save()
                pilotweek.save()
                skillset.save()