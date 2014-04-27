# Create your views here.
from genshi import Markup
from django_genshi import loader
from solaris.core import render_page
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def login_page(request):
    failed = False
    
    if (request.method == 'POST'):
        user = authenticate(
            username = request.POST['login'],
            password = request.POST['pass']
        )
        if user is not None:
            login(request, user)
            
            if 'redirect' in request.POST:
                return redirect(request.POST['redirect'])
            else:
                return redirect('/')
        else:
            failed = True
            
    if 'next' in request.GET:
        redirectURL = request.GET['next']
    else:
        redirectURL = None
              
    login_form = loader.get_template('userforms/login_form.tmpl')
    body = Markup(login_form.generate(failed=failed, redirect=redirectURL))  

    return render_page(body=body, selected=None, request=request)


def registration_page(request):
    if (request.method == 'POST'):
        print 'Form Received'
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print 'Form Validated'
            form.save()
            if 'redirect' in request.POST:
                return redirect(request.POST['redirect'])
            else:
                return redirect('/login')
        else:
            print form.errors
        
    else:
        form = RegistrationForm()
           
    return render_page(body=form.render(), selected=None, request=request)
    
def logout_user(request):
    logout(request)
    return redirect('/')