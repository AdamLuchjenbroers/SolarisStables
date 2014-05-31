from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ModelChoiceField

from .models import Pilot, PilotTraining

from solaris.warbook.pilotskill.models import PilotDiscipline

class PilotForm(ModelForm):

    class Meta:
        model = Pilot
        fields = ('pilot_name', 'pilot_callsign', 'pilot_rank', 'skill_gunnery', 'skill_pilotting', 'exp_character_points')
        
class PilotTrainingForm(ModelForm):
    
    discipline = ModelChoiceField(queryset=PilotDiscipline.objects.all())
    
    class Meta:
        model = PilotTraining
        fields = ('discipline', 'training', 'notes')        
        
PilotInlineSkillsForm = inlineformset_factory(Pilot, PilotTraining, form=PilotTrainingForm )