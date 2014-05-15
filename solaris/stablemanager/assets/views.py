from django.http import HttpResponse
from genshi import Markup

from solaris.stablemanager.views import StableView
from solaris.views import SolarisFormViewMixin

from .forms import PilotForm

class StablePilotsView(StableView):
    def get(self, request, stable=None):
        body = Markup('<P>The Pilots Listing for the %s will go here</P>' % stable.stable_name)
        return HttpResponse(self.in_layout(body, request))

class StableNewPilotsView(SolarisFormViewMixin, StableView):
    form_class = PilotForm
    form_properties = {
        'css-class' : 'pilotform'
    ,   'post-url'  : '/stable/pilots/add'
    ,   'submit'    : 'Submit'
    ,   'redirect'  : None
    }
    
    form_initial = {
        'pilot_rank' : 'Rookie'
    ,   'skill_gunnery' : 5
    ,   'skill_pilotting' : 6
    ,   'exp_character_points' : 0
    }
    
    def get(self, request, stable=None):
        form = self.get_form()
        formHTML = Markup(self.render_form(form))
        return HttpResponse( self.in_layout( formHTML , request))
    
    def post(self, request, stable=None):
        form = self.get_form(request.POST)
        formHTML = Markup(self.render_form(form))
        return HttpResponse( self.in_layout( formHTML , request))
        
    
    