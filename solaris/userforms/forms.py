from genshi import Markup
from django_genshi import loader
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput, ValidationError
from solaris.forms import SolarisModelForm, SolarisForm

class LoginForm(SolarisForm):
    username = CharField(label='Username', required=True)
    password = CharField(label='Password', widget=PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    
    
    def clean(self):
        super(LoginForm,self).clean()
        
        if not ('username' in self.cleaned_data and 'password' in self.cleaned_data):
            # A validation error will have already been raised for this
            # so we don't need to raise another
            return
        
        self.user = authenticate(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password']
        )
                
        if self.user == None:
            raise ValidationError('Invalid Username or Password')
        
class RegistrationForm(SolarisModelForm):
    
    passwordrepeat = CharField(widget=PasswordInput, label='Repeat')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        self.fields['email'].label = 'E-Mail'
        self.fields['password'].widget = PasswordInput()
           
    def clean(self):
        super(RegistrationForm,self).clean()
        
        if self.cleaned_data["password"] != self.cleaned_data["passwordrepeat"]:
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
        form_template = loader.get_template('solaris_form_outer.tmpl')

        return form_template.generate(form_items=Markup(self.as_p()), formclass='register', post_url='/register', submit='Register')
    
