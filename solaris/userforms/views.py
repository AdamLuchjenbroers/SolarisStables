# Create your views here.
from genshi import Markup
from django_genshi import loader
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from urlparse import urlparse
from django.http import HttpResponse

from .forms import RegistrationForm, LoginForm
from solaris.core import render_page
from solaris.views import SolarisView

class SolarisLoginView(SolarisView):
    
    def __init__(self, *args, **kwargs):
        super(SolarisLoginView, self).__init__(*args, **kwargs)
        self.template = loader.get_template('solaris_form_outer.tmpl')
    
    def post(self, request, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            
            if 'redirect' in request.POST:
                url = urlparse(request.POST['redirect'])
                return redirect(url.path)
            else:
                return redirect('/')
            
        body = Markup(self.template.generate(form_items=Markup(form.as_p()), formclass='login', post_url='/login', submit='Login'))         
        return HttpResponse(self.in_layout(body, request))
            
    def get(self, request, **kwargs):
        if 'next' in request.GET:
            url = urlparse(request.GET['next'])
            redirectURL = url.path
        else:
            redirectURL = None
        form = LoginForm()
        form.redirect = redirectURL  
        
        body = Markup(self.template.generate(form_items=Markup(form.as_p()), formclass='login', post_url='/login', submit='Login'))         
        return HttpResponse(self.in_layout(body, request))

class SolarisRegistrationView(SolarisView):
    
    def __init__(self, *args, **kwargs):
        super(SolarisRegistrationView, self).__init__(*args, **kwargs)
        self.template = loader.get_template('solaris_form_outer.tmpl')
    
    def post(self, request, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if 'redirect' in request.POST:
                url = urlparse(request.POST['redirect'])
                return redirect(url.path)
            else:
                return redirect('/login')
            
    
    def get(self, request, **kwargs):
        form = RegistrationForm()
           
        body = Markup(self.template.generate(form_items=Markup(form.as_p()), formclass='registration', post_url='/register', submit='Register'))         
        return HttpResponse(self.in_layout(body, request))
            
def logout_user(request):
    logout(request)
    return redirect('/')