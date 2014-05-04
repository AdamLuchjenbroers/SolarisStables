# Create your views here.
from genshi import Markup
from django_genshi import loader
from solaris.core import render_page
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect

def login_page(request):
    
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            
            if 'redirect' in request.POST:
                return redirect(request.POST['redirect'])
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
                return redirect(request.POST['redirect'])
            else:
                return redirect('/login')
        
    else:
        form = RegistrationForm()
           
    return render_page(body=form.render(), selected=None, request=request)
    
def logout_user(request):
    logout(request)
    return redirect('/')