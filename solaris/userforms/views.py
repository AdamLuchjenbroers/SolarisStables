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
    
    passwordrepeat = CharField(widget=PasswordInput, label='Repeat')
    password = CharField(widget=PasswordInput)
    # Eliminate the blurb about valid user names
    username = CharField()
    email=CharField(label='E-Mail')
    
    def clean(self):
        super(RegistrationForm,self).clean()
        
        if self.cleaned_data.get('password') != self.cleaned_data.get('passwordrepeat'):
            print self.cleaned_data
            raise ValidationError('Passwords entered do not match')
       
        return self.cleaned_data
              
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user  
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'passwordrepeat' )
        
    def render(self):
        form_template = loader.get_template('userforms/register.tmpl')

        return form_template.generate(form_items=Markup(self.as_p()),redirect=None)
    

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