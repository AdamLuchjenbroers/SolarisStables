from django.forms.models import BaseInlineFormSet, inlineformset_factory

from solaris.forms import SolarisModelForm, SolarisInlineForm

from .models import Pilot, PilotTraining

class PilotForm(SolarisModelForm):

    class Meta:
        model = Pilot
        fields = ('pilot_name', 'pilot_callsign', 'pilot_rank', 'skill_gunnery', 'skill_pilotting', 'exp_character_points')
        
class PilotTrainingForm(SolarisInlineForm):
    
    class Meta:
        model = PilotTraining
        
        
PilotInlineSkillsForm = inlineformset_factory(Pilot, PilotTraining, form=PilotTrainingForm )