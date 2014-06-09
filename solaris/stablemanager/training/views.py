from django.views.generic import TemplateView
from django.shortcuts import get_list_or_404

from solaris.stablemanager.views import StableWeekMixin
from solaris.stablemanager.assets.models import PilotWeek

class StableTrainingView(StableWeekMixin, TemplateView):
    submenu_selected = 'Training'
    template_name = 'stablemanager/stable_training.tmpl'
    
    def get_context_data(self, **kwargs):
        page_context = super(StableTrainingView, self).get_context_data(**kwargs)
        
        page_context['object_list'] = get_list_or_404(PilotWeek, pilot__stable=self.stable, week=self.week)
        return page_context
        
