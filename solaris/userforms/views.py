# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from urlparse import urlparse
from django.views.generic import FormView, CreateView

from .forms import RegistrationForm, LoginForm
from solaris.views import SolarisViewMixin

class SolarisLoginView(SolarisViewMixin, FormView):
    template_name = 'solaris_basicform.tmpl'
    form_class = LoginForm
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        page_context = super(SolarisLoginView, self).get_context_data(**kwargs)
        
        page_context['post_url'] = '/login'
        page_context['submit'] = 'Login'
        page_context['form_class'] = 'login'
        
        return page_context
    
    def form_valid(self, form):
        login(self.request, form.user)
        return super(SolarisLoginView, self).form_valid(form)
        
    def get(self, request):
        if 'next' in request.GET:
            url = urlparse(request.GET['next'])
            self.success_url = url.path
        
        return super(SolarisLoginView, self).get(request)        
    
class SolarisRegistrationView(SolarisViewMixin, CreateView):   
    template_name = 'solaris_basicform.tmpl'
    form_class = RegistrationForm
    success_url = '/'
    model = User
    
    def get_context_data(self, **kwargs):
        page_context = super(SolarisRegistrationView, self).get_context_data(**kwargs)
        
        page_context['post_url'] = '/register'
        page_context['submit'] = 'Register'
        page_context['form_class'] = 'registration'
        
        return page_context
            
def logout_user(request):
    logout(request)
    return redirect('/')