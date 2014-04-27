# Create your views here.
from genshi import Markup
from django_genshi import loader
from solaris.core import render_page
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, ValidationError
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


class RegistrationForm(ModelForm):
    password = CharField(widget=PasswordInput)
    passwordrepeat = CharField(widget=PasswordInput, label='Repeat Password')
    
    def clean_password(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('passwordrepeat'):
            raise ValidationError('Passwords entered do not match')
        
        
    def is_valid(self):
        if not super(RegistrationForm,self).is_valid():
            return False
        
        if self.password != self.passwordrepeat:
            self.add_error('password','Passwords entered do not match')
            return False
        
        return True        
        
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'passwordrepeat' )
        
    def render(self):
        form_template = loader.get_template('userforms/register.tmpl')

        return form_template.generate(form_items=Markup(self.as_p()),redirect=None)
    

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