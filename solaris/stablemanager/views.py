from genshi import Markup
from django_genshi import loader
from django.http import HttpResponse

from solaris.views import SolarisView
from solaris.core import render_page
from .utils import stable_required


from .forms import StableRegistrationForm

class StableView(SolarisView):
    def get_submenu(self):
        return [
          {'title' : 'Ledger', 'url' : '/stable/ledger'},
          {'title' : 'Assets', 'url' : '/stable'},
          {'title' : 'Actions', 'url' : '/stable/actions'},
          {'title' : 'Training', 'url' : '/stable/training'},          
        ]
    
    @stable_required(add_stable=True)
    def dispatch(self, request, *args, **kwargs):
        self.stable = kwargs['stable']
        return super(StableView, self).dispatch(request, *args, **kwargs)

class StableOverview(StableView):    
    def get(self, request, stable=None):
        body = Markup('<P>Stable Management for the %s will go here</P>' % stable.stable_name)
        return HttpResponse(self.in_layout(body, request))
    

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
