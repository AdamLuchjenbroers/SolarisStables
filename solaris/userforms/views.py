# Create your views here.
from genshi import Markup
from django_genshi import loader
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from urlparse import urlparse

from .forms import RegistrationForm, LoginForm
from solaris.core import render_page

def login_page(request):
    
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            
            if 'redirect' in request.POST:
                url = urlparse(request.POST['redirect'])
                return redirect(url.path)
            else:
                return redirect('/')
    else:
        if 'next' in request.GET:
            redirectURL = request.GET['next']
        else:
            redirectURL = None
        form = LoginForm()
        form.redirect = redirectURL   
              
    login_form = loader.get_template('solaris_form_outer.tmpl')
    body = Markup(login_form.generate(form_items=Markup(form.as_p()), formclass='login', post_url='/login', submit='Login')) 

    return render_page(body=body, selected=None, request=request)


def registration_page(request):
    if (request.method == 'POST'):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if 'redirect' in request.POST:
                url = urlparse(request.POST['redirect'])
                return redirect(url.path)
            else:
                return redirect('/login')
        
    else:
        form = RegistrationForm()
           
    return render_page(body=form.render(), selected=None, request=request)
    
def logout_user(request):
    logout(request)
    return redirect('/')