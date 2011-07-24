# Create your views here.
from genshi import Markup
from django_genshi import loader
from solaris.core import render_page
from django.contrib.auth import authenticate, login
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
	    redirect('/')
	else:
            failed = True
              
    login_form = loader.get_template('login_form.tmpl')
    body = Markup(login_form.generate(failed=failed))  

    return render_page(body=body, selected=None, request=request)


def registration_page(request):
    body = Markup('<P>This will be the Registration page</P>')
    return render_page(body=body, selected=None, request=request)