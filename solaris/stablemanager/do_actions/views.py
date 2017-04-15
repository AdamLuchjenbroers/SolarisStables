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

        page_context['actionform'] = forms.StableActionForm(stableweek=self.stableweek)

        page_context['ap_spent'] = self.stableweek.actions.spent_actions() 
        page_context['ap_avail'] = self.week.campaign.actions_per_week

        if self.stableweek.week_started:
            page_context['count_mechs']  = self.stableweek.mechs_count
            page_context['count_pilots'] = self.stableweek.pilot_count
            page_context['count_assets'] = self.stableweek.asset_count
        else:
            page_context['count_mechs'] = self.stableweek.mechs.count_nonsignature()
            page_context['count_pilots'] = self.stableweek.pilots.all_present().count()
            page_context['count_assets'] = page_context['count_mechs'] + page_context['count_pilots']
 
        return page_context

class StableActionListPart(StableActionView):
    template_name = 'stablemanager/fragments/actions_list.html'

class StableManagementPart(StableActionView):
    template_name = 'stablemanager/fragments/action_management.html'

class StableActionFormView(StableWeekMixin, FormView):
    submenu_selected = 'Actions'
    template_name = 'stablemanager/forms/add_action_form.html'
    form_class = forms.StableActionForm

    def get_form_kwargs(self):
        kwargs = super(StableActionFormView, self).get_form_kwargs()

        kwargs['stableweek'] = self.stableweek
        return kwargs

    def post(self, request, week=None):
        form = forms.StableActionForm(request.POST)

        if form.is_valid():
            form.save(commit = False)
    
            form.instance.week = self.stableweek
            form.instance.save()

            return HttpResponse(json.dumps(True))
        else:
            return HttpResponse(form.errors.as_json())
    
    def get_context_data(self, **kwargs):            
        page_context = super(StableActionFormView, self).get_context_data(**kwargs)

        return page_context

class AjaxActionMixin(StableWeekMixin, SingleObjectMixin):
    def get_queryset(self):
        return self.stableweek.actions.all()

    def dispatch(self, request, *args, **kwargs):
        # Wrap all requests with this exception handler so handling of missing or 
        # incorrect query parameters is consistent
        try:
            return super(AjaxActionMixin, self).dispatch(request, *args, **kwargs)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

    def render_to_json(self, action):
        data = {
          'action'    : action.action.action
        , 'action_id' : action.id
        , 'cost'      : action.cost
        , 'notes'     : action.notes
        }
        return HttpResponse(json.dumps(data))

class AjaxRemoveAction(AjaxActionMixin, View):
    def post(self, request, week=None, pk=None):
        action = self.get_object()
        action.delete()

        return HttpResponse(json.dumps(True))

class AjaxSetActionCost(AjaxActionMixin, View):
    def post(self, request, week=None, pk=None):
        action = self.get_object()

        if action.is_locked():
            return HttpResponse('Cannot Set Cost - Action Locked', status=400)
 
        action.cost = int(request.POST['cost'])
        action.save()
  
        return self.render_to_json(action) 

class AjaxSetActionNotes(AjaxActionMixin, View):
    def post(self, request, week=None, pk=None):
        action = self.get_object()
        action.notes = request.POST['notes']
        action.save()

        return self.render_to_json(action) 

class AjaxSetWeekStarted(StableWeekMixin, View):
    def post(self, request, week=None):
        postdata = request.POST.get('start_week', 'TRUE')
        started = ( postdata.upper() == 'TRUE' )

        if started:
            self.stableweek.start_week()
        else:
            self.stableweek.reset_week()

        return HttpResponse(json.dumps(True))

   
