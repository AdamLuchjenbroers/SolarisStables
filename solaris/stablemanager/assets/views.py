from django.http import HttpResponse
from genshi import Markup
from django_genshi import loader

from solaris.stablemanager.views import StableView

from .forms import PilotForm, PilotInlineSkillsForm

class StablePilotsView(StableView):
    def get(self, request, stable=None):
        body = Markup('<P>The Pilots Listing for the %s will go here</P>' % stable.stable_name)
        return HttpResponse(self.in_layout(body, request))

class StableNewPilotsView(StableView):
    form_properties = {
        'css_class' : 'pilotform'
    ,   'post_url'  : '/stable/pilots/add'
    ,   'submit'    : 'Submit'
    ,   'redirect'  : None
    }
    
    form_initial = {
        'pilot_rank' : 'Rookie'
    ,   'skill_gunnery' : 5
    ,   'skill_pilotting' : 6
    ,   'exp_character_points' : 0
    }
    
    def __init__(self):
        self.template = loader.get_template('stablemanager/pilot_form.genshi')
        super(StableNewPilotsView, self).__init__()
        
    
    def get(self, request, stable=None):
        frm_pilot = PilotForm()
        frm_skills = PilotInlineSkillsForm()
        
        html_pilot = Markup(frm_pilot.as_p())
        html_skills = Markup(frm_skills.as_p())
        
        rendered = self.template.generate(pilot_form=html_pilot, skills_form=html_skills, **self.__class__.form_properties )
        
        formHTML = Markup(rendered)
        return HttpResponse( self.in_layout( formHTML , request))
    
    def post(self, request, stable=None):
        form = self.get_form(request.POST)
        formHTML = Markup(self.render_form(form))
        return HttpResponse( self.in_layout( formHTML , request))
        
    
    