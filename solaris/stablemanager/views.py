from genshi import Markup
from django_genshi import loader
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import TemplateView, CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login


from solaris.views import SolarisView, SolarisViewMixin
from solaris.battlereport.models import BroadcastWeek

from .models import Stable
from .utils import stable_required
from .forms import StableRegistrationForm

class StableView(SolarisView):
    submenu = [
          {'title' : 'Ledger', 'url' : '/stable/ledger'},
          {'title' : 'Assets', 'url' : '/stable'},
          {'title' : 'Actions', 'url' : '/stable/actions'},
          {'title' : 'Training', 'url' : '/stable/training'},
          {'title' : 'Pilots', 'url' : '/stable/pilots'},          
        ]
    menu_selected = 'Stable'
    
    @stable_required(add_stable=True)
    def dispatch(self, request, *args, **kwargs):
        self.stable = kwargs['stable']
        return super(StableView, self).dispatch(request, *args, **kwargs)

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
    form_class = CreateView
    template_name = 'stablemanager/stable_register.tmpl'
    success_url = '/stable'
    
    def get_context_data(self, **kwargs):
        page_context = super(StableRegistrationView, self).get_context_data(**kwargs)
        
        page_context['post_url'] = reverse ('stable_registration')
        page_context['submit'] = 'Register'
        page_context['form_class'] = 'registration'
        
        return page_context

class OldStableRegistrationView(SolarisView):    
    scripts_list = ['/static/js/jquery-1.11.1.js', '/static/js/stable_registration.js']
    
    def __init__(self, *args, **kwargs):
        super(StableRegistrationView, self).__init__(*args, **kwargs)
        
        self.template = loader.get_template('stablemanager/register.genshi')
    
    def get_scripts(self):
        return ['/static/js/jquery-1.11.1.js', '/static/js/stable_registration.js']
    
    def create_stable(self, form, request):
        form.register_stable(request.user)       
            
        return redirect('/stable')
    
    def get(self, request):
        form = StableRegistrationForm()
        body = self.template.generate(form_items=Markup(form.as_p()))
        
        return HttpResponse( self.in_layout(body, request) )        
    
    def post(self, request):
        form = CreateView(request.POST)
        body = self.template.generate(form_items=Markup(form.as_p()))
        if form.is_valid():
            return self.create_stable(form, request)
        else:       
            return HttpResponse( self.in_layout(body, request) )   
