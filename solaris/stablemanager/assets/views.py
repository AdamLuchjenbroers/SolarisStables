from genshi import Markup
from django_genshi import loader

from django.http import HttpResponse
from django.views.generic import TemplateView, FormView

from solaris.stablemanager.views import StableWeekMixin

from .forms import PilotForm, PilotInlineSkillsForm

class StablePilotsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/stable_pilots.tmpl'

class StableNewPilotsView(StableViewMixin, View):
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
        
    
    
