from django.views.generic import View, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
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

        page_context['start_list'] = self.stableweek.actions.start_of_week()
        page_context['inweek_list'] = self.stableweek.actions.in_week()

        page_context['ap_spent']
        page_context['ap_avail'] = 
 
        return page_context

class StableActionListPart(StableActionView):
    template_name = 'stablemanager/fragments/actions_list.html'

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

        return page_context

class AjaxRemoveAction(StableWeekMixin, SingleObjectMixin, View):
    def get_queryset(self):
        return self.stableweek.actions.all()

    def post(self, request, week=None, pk=None):
        action = self.get_object()
        action.delete()

        return HttpResponse(json.dumps(True)) 
