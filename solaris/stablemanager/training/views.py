from django.views.generic import ListView
from django.shortcuts import get_list_or_404

from solaris.stablemanager.views import StableWeekMixin
from solaris.stablemanager.mechs.models import PilotWeek

class StableTrainingView(StableWeekMixin, ListView):
    submenu_selected = 'Training'
    template_name = 'stablemanager/stable_training.tmpl'
    
    def get_queryset(self, **kwargs):
        return get_list_or_404(PilotWeek, pilot__stable=self.stable, week=self.week)
        
