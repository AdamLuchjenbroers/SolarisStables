from genshi import Markup
from django_genshi import loader
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, ValidationError

class RegistrationForm(ModelForm):
    
    passwordrepeat = CharField(widget=PasswordInput, label='Repeat')
    password = CharField(widget=PasswordInput)
    # Eliminate the blurb about valid user names
    username = CharField()
    email=CharField(label='E-Mail')
    
    def clean(self):
        super(RegistrationForm,self).clean()
        
        if self.cleaned_data["password"] != self.cleaned_data["passwordrepeat"]:
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
    