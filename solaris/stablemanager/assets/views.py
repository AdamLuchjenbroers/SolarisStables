from genshi import Markup
from django_genshi import loader

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin

from .forms import PilotForm, PilotInlineSkillsForm

class StablePilotsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/stable_pilots.tmpl'

class StableNewPilotsView(StableViewMixin, TemplateView):
    submenu_selected = 'Pilots'
    template_name = 'stablemanager/forms/add_pilot.tmpl'
    
    def __init__(self):
        self.form_pilot = PilotForm(initial={
            'pilot_rank' : 'Rookie'
        ,   'skill_gunnery' : 5
        ,   'skill_pilotting' : 6
        ,   'exp_character_points' : 0
        })
        self.form_skills = PilotInlineSkillsForm()
    
    def get_context_data(self, **kwargs):
        page_context = super(StableNewPilotsView, self).get_context_data(**kwargs)
        
        page_context['pilot'] = self.form_pilot
        page_context['skillset'] = self.form_skills
        
        page_context['post_url'] = reverse ('pilots_add')
        page_context['submit'] = 'Add'
        page_context['form_class'] = 'pilot'
        
        return page_context
    
class OldStableNewPilotsView(object):
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
        
    
    
