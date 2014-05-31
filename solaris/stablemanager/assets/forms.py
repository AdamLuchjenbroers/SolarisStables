from django.forms.models import inlineformset_factory
from django.forms import ModelForm

from .models import Pilot, PilotTraining

class PilotForm(ModelForm):

    class Meta:
        model = Pilot
        fields = ('pilot_name', 'pilot_callsign', 'pilot_rank', 'skill_gunnery', 'skill_pilotting', 'exp_character_points')
        
class PilotTrainingForm(ModelForm):
    
    class Meta:
        model = PilotTraining        
        
PilotInlineSkillsForm = inlineformset_factory(Pilot, PilotTraining, form=PilotTrainingForm )