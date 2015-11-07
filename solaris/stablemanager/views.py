
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import TemplateView, CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

from solaris.views import SolarisViewMixin
from solaris.campaign.models import BroadcastWeek
from solaris.warbook.pilotskill.models import PilotDiscipline

from .models import Stable
from .ledger.models import Ledger
from .forms import StableRegistrationForm

class StableViewMixin(SolarisViewMixin):
    menu_selected = 'Stable'
    
    def get_context_data(self, **kwargs):
        page_context = super(StableViewMixin, self).get_context_data(**kwargs)
        
        page_context['stable'] = self.stable
        page_context['selected'] = 'Stable'
        page_context['submenu'] = [
          {'title' : 'Ledger', 'url' : '/stable/ledger'},
          {'title' : 'Assets', 'url' : '/stable'},
          {'title' : 'Actions', 'url' : '/stable/actions'},
          {'title' : 'Training', 'url' : '/stable/training'},
          {'title' : 'Pilots', 'url' : '/stable/pilots'},          
        ]
        
        return page_context
    
    def get_stable(self, request):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'login', REDIRECT_FIELD_NAME)

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
    def dispatch(self, request, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect        
        
        if 'week' in self.kwargs:
            self.week = get_object_or_404(BroadcastWeek, week_number=self.kwargs['week'])
        else:
            self.week = self.stable.current_week
                   
        return super(StableWeekMixin, self).dispatch(request, *args, **kwargs) 
    
    
    def get_context_data(self, **kwargs):
        page_context = super(StableWeekMixin, self).get_context_data(**kwargs)
        page_context['week'] = self.week        
 
        return page_context            

class StableOverview(StableViewMixin, TemplateView):       
    submenu_selected = 'Assets'
    template_name = 'stablemanager/stable_overview.tmpl'

class StableRegistrationView(SolarisViewMixin, CreateView):
    menu_selected = 'Stable'
    form_class = StableRegistrationForm
    template_name = 'stablemanager/stable_register.tmpl'
    success_url = '/stable'
    model = Stable
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()           
                    
        self.object.stable_disciplines.add( PilotDiscipline.objects.get(name=form.cleaned_data['discipline_1']) )
        self.object.stable_disciplines.add( PilotDiscipline.objects.get(name=form.cleaned_data['discipline_2']) )
        self.object.save()
    
    def get_context_data(self, **kwargs):
        page_context = super(StableRegistrationView, self).get_context_data(**kwargs)
        
        page_context['post_url'] = reverse ('stable_registration')
        page_context['submit'] = 'Register'
        page_context['form_class'] = 'registration'
        
        return page_context
