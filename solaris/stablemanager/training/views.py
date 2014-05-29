from django.views.generic import TemplateView

from solaris.stablemanager.views import StableWeekMixin

class StableTrainingView(StableWeekMixin, TemplateView):
    submenu_selected = 'Training'
    template_name = 'stablemanager/stable_training.tmpl'
        
