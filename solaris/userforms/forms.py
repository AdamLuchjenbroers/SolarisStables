from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput, ValidationError
from django.forms import ModelForm, Form

class LoginForm(Form):
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
        
        return self.cleaned_data
        
class RegistrationForm(ModelForm):
    
    passwordrepeat = CharField(widget=PasswordInput, label='Repeat', required=True)
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        self.fields['email'].label = 'E-Mail'
        self.fields['password'].widget = PasswordInput()
        self.fields['password'].required = True

    def clean(self):
        super(RegistrationForm,self).clean()
        
        if not('password' in self.cleaned_data.keys() and 'passwordrepeat' in self.cleaned_data.keys()):
            # Already caught elsewhere
            return self.cleaned_data
        elif self.cleaned_data["password"] != self.cleaned_data["passwordrepeat"]:
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
    
