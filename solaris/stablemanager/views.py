
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 

import json

from solaris.views import SolarisViewMixin
from solaris.campaign.models import BroadcastWeek, Campaign
from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.warbook.techtree.models import Technology

from .models import Stable
from .ledger.models import StableWeek
from .forms import StableRegistrationForm

class StableViewMixin(SolarisViewMixin):
    menu_selected = 'Stable'
    
    def get_context_data(self, **kwargs):
        page_context = super(StableViewMixin, self).get_context_data(**kwargs)
        
        page_context['stable'] = self.stable
        page_context['selected'] = 'Stable'
        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('stable_overview_now')},
          {'title' : 'Finances', 'url' : reverse('stable_ledger_now')},
#          {'title' : 'Training', 'url' : reverse('stable_training_now')},
          {'title' : 'Mechs', 'url' : reverse('stable_mechs_now')},   
          {'title' : 'Pilots', 'url' : reverse('stable_pilots_now')},    
          {'title' : 'Actions', 'url' : reverse('stable_actions_now')},      
        ]
        page_context['submenu_selected'] = self.__class__.submenu_selected
        
        return page_context

    def get_stable(self, request):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        try:
            self.stable = Stable.objects.get(owner=request.user)
            return None
        except Stable.DoesNotExist:
            return redirect(reverse ('stable_registration'))        
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'stable'):
            # get_stable hasn't already been called
            redirect = self.get_stable(request)
            if redirect:
                return redirect
        
        return super(StableViewMixin, self).dispatch(request, *args, **kwargs)

class StableWeekMixin(StableViewMixin):
    """
      StableWeekMixin handles Stable Views that vary on a week-by-week basis.
      If week is provided as a parameter, the provided week is used otherwise
      the view defaults to the current Stable Week
    """
    # Should this view enable the current week to be changed.
    week_navigation = True
    view_url_name = 'stable_overview'

    def prev_week_url(self):
        if self.stableweek.has_prev_week():
            prev_week_no = self.stableweek.prev_week.week.week_number
            return reverse(self.__class__.view_url_name, kwargs={'week' : prev_week_no})
        else:
            return None

    def next_week_url(self):
        if self.stableweek.next_week != None:
            next_week_no = self.stableweek.next_week.week.week_number
            return reverse(self.__class__.view_url_name, kwargs={'week' : next_week_no})
        else:
            return None

    def next_week_available(self):
        return (self.stableweek.week.next_week != None)

    def get_stableweek(self):
        if 'week' in self.kwargs:
            self.week = get_object_or_404(BroadcastWeek, week_number=self.kwargs['week'])
            self.stableweek = get_object_or_404(StableWeek, stable=self.stable, week=self.week)
        else:
            self.stableweek = self.stable.get_stableweek()
            self.week = self.stableweek.week

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'stable'):
            # get_stable hasn't already been called
            redirect = self.get_stable(request)
            if redirect:
                return redirect
        
        if not hasattr(self, 'stableweek'):
            # get_stableweek hasn't already been called
            self.get_stableweek()
                   
        return super(StableWeekMixin, self).dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        page_context = super(StableWeekMixin, self).get_context_data(**kwargs)
        page_context['stableweek'] = self.stableweek        
        page_context['week'] = self.week
        page_context['week_navigation'] = self.__class__.week_navigation        

        week_args = { 'week' : self.week.week_number }
        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('stable_overview', kwargs=week_args)},
          {'title' : 'Finances', 'url' : reverse('stable_ledger', kwargs=week_args)},
#          {'title' : 'Training', 'url' : reverse('stable_training', kwargs=week_args)},
          {'title' : 'Mechs', 'url' : reverse('stable_mechs', kwargs=week_args)},   
          {'title' : 'Pilots', 'url' : reverse('stable_pilots', kwargs=week_args)},    
          {'title' : 'Actions', 'url' : reverse('stable_actions', kwargs=week_args)},      
        ]
 
        page_context['prev_week_url'] = self.prev_week_url()
        page_context['next_week_url'] = self.next_week_url()
        page_context['view_url_name'] = self.__class__.view_url_name

        return page_context            

class StableOverview(StableWeekMixin, TemplateView):       
    submenu_selected = 'Overview'
    template_name = 'stablemanager/stable_overview.tmpl'

class StableRegistrationView(SolarisViewMixin, CreateView):
    menu_selected = 'Stable'
    form_class = StableRegistrationForm
    template_name = 'stablemanager/stable_register.tmpl'
    success_url = '/stable/initial-mechs'
    model = Stable
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.campaign = Campaign.objects.get_current_campaign()   

        self.object.save()

        for discipline in form.cleaned_data.get('stable_disciplines'):                    
            self.object.stable_disciplines.add(discipline)
            
        self.object.save()
        return super(StableRegistrationView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        page_context = super(StableRegistrationView, self).get_context_data(**kwargs)
        
        page_context['post_url'] = reverse ('stable_registration')
        page_context['submit'] = 'Register'
        page_context['form_class'] = 'registration'
        
        return page_context

class StableTechListPart(StableWeekMixin, TemplateView):
    template_name = 'stablemanager/fragments/stable_tech_list.html'

    def get_context_data(self, **kwargs):
        page_context = super(StableTechListPart, self).get_context_data(**kwargs)
        
        page_context['techlist'] = self.stableweek.supply_contracts.all()
        
        return page_context
  
class AjaxAddStableTech(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            tech = get_object_or_404(Technology, name=request.POST['tech'])
            self.stableweek.add_technology(tech)

            return HttpResponse(json.dumps(True))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)

class AjaxAlterReputationView(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            if request.POST['change'] == 'plus':
                self.stableweek.reputation += 1
            elif request.POST['change'] == 'minus':
                self.stableweek.reputation -= 1
            else:
                return HttpResponse('Unrecognised Action: %s' % request.POST['change'], status=400)

            self.stableweek.reputation_set = True            
            self.stableweek.save()
            data = { 
              'value' : self.stableweek.reputation 
            , 'text'  : self.stableweek.reputation_text() 
            , 'class' : self.stableweek.reputation_class() 
            }
              
            return HttpResponse(json.dumps(data))

        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
    

class AjaxCreateStableWeekView(StableWeekMixin, View):
    def post(self, request, week=None):
        view = self.__class__.view_url_name
        if 'view' in request.POST:
            view = request.POST['view']

        try:
            week_no = int(request.POST['week'])
            week = self.stable.get_stableweek(week=week_no)

            nextweek = week.advance()
            nexturl = reverse(view, kwargs={'week' : nextweek.week.week_number})

            return HttpResponse(json.dumps(nexturl))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except StableWeek.DoesNotExist:
            return HttpResponse('Source Stable Week not found', status=404)
