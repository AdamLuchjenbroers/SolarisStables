from genshi import Markup
from django_genshi import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse


from solaris.views import SolarisView
from solaris.core import render_page
from solaris.stablemanager.models import Stable


from .forms import StableRegistrationForm

@login_required(login_url='/login')
def stable_main(request):
    
    stableList = Stable.objects.filter(owner = request.user)
    
    if len(stableList) <> 1:
        return redirect('/stable/register')
            
    stable = stableList[0]
            
    body = Markup('<P>Stable Management for the %s will go here</P>' % stable.stable_name )
    return render_page(body=body, selected=None, request=request)


class StableRegistrationView(SolarisView):
    
    def __init__(self, *args, **kwargs):
        super(StableRegistrationView, self).__init__(*args, **kwargs)
        
        self.template = loader.get_template('stablemanager/register.tmpl')
    
    def create_stable(self, form, request):
        form.register_stable(request.user)       
            
        return HttpResponse(self.in_layout('<p>Valid Form</p>', request))
    
    def get(self, request):
        form = StableRegistrationForm()
        body = self.template.generate(form_items=Markup(form.as_p()))
        
        return HttpResponse( self.in_layout(body, request) )        
    
    def post(self, request):
        form = StableRegistrationForm(request.POST)
        body = self.template.generate(form_items=Markup(form.as_p()))
        if form.is_valid():
            return self.create_stable(form, request)
        else:       
            return HttpResponse( self.in_layout(body, request) )   
    #    pass
        
    

def stable_registration(request):
    body = Markup('<P>This will become a Stable Registration Page</P>')
    return render_page(body=body, selected=None, request=request)
