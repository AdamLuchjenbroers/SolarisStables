from django.views.generic import TemplateView

from solaris.stablemanager.views import StableWeekMixin

class StableOptionsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Options'
    template_name = 'stablemanager/stable_options.html'
    view_url_name = 'stable_options'
