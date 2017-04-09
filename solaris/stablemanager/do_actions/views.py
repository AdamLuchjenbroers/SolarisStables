from django.views.generic import TemplateView, FormView
from django.http import HttpResponse

import json

from solaris.stablemanager.views import StableWeekMixin
from . import forms, models

class StableActionView(StableWeekMixin, TemplateView):
    submenu_selected = 'Actions'
    template_name = 'stablemanager/stable_actions.tmpl'
    view_url_name = 'stable_actions'

    def get_context_data(self, **kwargs):
        page_context = super(StableActionView, self).get_context_data(**kwargs)

        page_context['actionform'] = forms.StableActionForm()
        page_context['week_no'] = self.stableweek.week.week_number

        page_context['start_list'] = self.stableweek.actions.start_of_week()
        page_context['inweek_list'] = self.stableweek.actions.in_week()

        return page_context

class StableActionListPart(StableWeekMixin, TemplateView):
    template_name = 'stablemanager/fragments/actions_list.html'

    def get_context_data(self, **kwargs):
        page_context = super(StableActionListPart, self).get_context_data(**kwargs)

        page_context['start_list'] = self.stableweek.actions.start_of_week()
        page_context['inweek_list'] = self.stableweek.actions.in_week()
        return page_context

class StableActionFormView(StableWeekMixin, FormView):
    submenu_selected = 'Actions'
    template_name = 'stablemanager/forms/add_action_form.html'
    form_class = forms.StableActionForm

    def post(self, request, week=None):
        form = forms.StableActionForm(request.POST)

        if form.is_valid():
            form.save(commit = False)
    
            form.instance.week = self.stableweek
            form.instance.save()

        return HttpResponse(json.dumps(True))
    
    def get_context_data(self, **kwargs):            
        page_context = super(StableActionFormView, self).get_context_data(**kwargs)

        page_context['week_no'] = self.stableweek.week.week_number
        return page_context
