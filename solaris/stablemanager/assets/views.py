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
    template_name = 'stablemanager/forms/add_pilot.tmpl'

    def get_context_data(self, **kwargs):
        page_context = super(StableNewPilotsView, self).get_context_data(**kwargs)
        
        page_context['pilot'] = forms.PilotForm(initial={
            'stable' : self.stable.id
        ,   'affiliation' : self.stable.house.id
        })
        
        page_context['pilotweek'] = forms.PilotWeekForm(initial={
            'pilot_rank' : PilotRank.objects.get(rank='Rookie')
        ,   'skill_gunnery' : 5
        ,   'skill_pilotting' : 6
        ,   'start_character_points' : 0
        ,   'week' : self.stable.current_week
        })
        
        page_context['skillset'] = forms.PilotInlineSkillsForm()
        
        page_context['post_url'] = reverse ('pilots_add')
        page_context['submit'] = 'Add'
        page_context['form_class'] = 'pilot'
        
        return page_context