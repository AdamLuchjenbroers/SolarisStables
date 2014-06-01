from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ModelChoiceField, HiddenInput

from . import models

from solaris.warbook.pilotskill.models import PilotTraitGroup

class PilotForm(ModelForm):
    
    def __init__(self, **kwargs):
        super(PilotForm, self).__init__(**kwargs)
        self.fields['stable'].widget = HiddenInput()
        
        self.fields['pilot_name'].label = 'Name'
        self.fields['pilot_callsign'].label = 'Callsign'

    class Meta:
        model = models.Pilot
        fields = ('stable','pilot_name', 'pilot_callsign','affiliation')
        
class PilotWeekForm(ModelForm):
    
    def __init__(self, **kwargs):
        super(PilotWeekForm, self).__init__(**kwargs)
        
        self.fields['pilot'].widget = HiddenInput()
        self.fields['week'].widget = HiddenInput()
        
        self.fields['start_character_points'].label = 'Experience'
        self.fields['skill_gunnery'].label = 'Gunnery'
        self.fields['skill_piloting'].label = 'Piloting'
    
    class Meta:
        model = models.PilotWeek
        fields = ('pilot', 'week','rank','skill_gunnery', 'skill_piloting', 'start_character_points')
    
        
class PilotTrainingForm(ModelForm):
    
    discipline = ModelChoiceField(queryset=PilotTraitGroup.objects.all())
    
    class Meta:
        model = models.PilotTraining
        fields = ('discipline', 'training', 'notes')        
        
PilotInlineSkillsForm = inlineformset_factory(models.PilotWeek, models.PilotTraining, form=PilotTrainingForm )