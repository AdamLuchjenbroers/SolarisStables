from django.views.generic import TemplateView

from solaris.stablemanager.views import StableWeekMixin

class StableActionView(StableWeekMixin, TemplateView):
    submenu_selected = 'Actions'
    template_name = 'stablemanager/stable_actions.tmpl'
    view_url_name = 'stable_actions'
        
