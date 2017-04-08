from django.views.generic import TemplateView

from solaris.stablemanager.views import StableWeekMixin
from . import forms, models

class StableActionView(StableWeekMixin, TemplateView):
    submenu_selected = 'Actions'
    template_name = 'stablemanager/stable_actions.tmpl'
    view_url_name = 'stable_actions'

    def get_context_data(self, **kwargs):
        page_context = super(StableActionView, self).get_context_data(**kwargs)

        page_context['actionform'] = forms.StableActionForm()

        return page_context

            
