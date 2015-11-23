from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ModelChoiceField, HiddenInput, CharField, modelformset_factory

from . import models

from solaris.warbook.pilotskill.models import PilotTraitGroup

class PilotForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PilotForm, self).__init__(*args, **kwargs)
        self.fields['stable'].widget = HiddenInput()
        self.fields['stable'].required = False #Will be set by invoking form
        
        self.fields['pilot_name'].label = 'Name'
        self.fields['pilot_callsign'].label = 'Callsign'

    class Meta:
        model = models.Pilot
        fields = ('stable','pilot_name', 'pilot_callsign','affiliation')

class PilotNamingForm(ModelForm):
    pilot_name = CharField(required=False)

    class Meta:
        model = models.Pilot
        fields = ('pilot_name', 'pilot_callsign')

    def summary(self):
        sw = self.instance.stable.get_stableweek()
        pw = self.instance.weeks.get(week=sw)
        return '%s, %i/%i' % (pw.rank.rank, pw.skill_gunnery, pw.skill_piloting)

PilotNamingFormSet = modelformset_factory(models.Pilot, form=PilotNamingForm, fields=('pilot_name', 'pilot_callsign'), extra=0)
        
class PilotWeekForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PilotWeekForm, self).__init__(*args, **kwargs)
        
        self.fields['start_character_points'].label = 'Experience'
        self.fields['skill_gunnery'].label = 'Gunnery'
        self.fields['skill_piloting'].label = 'Piloting'
    
    class Meta:
        model = models.PilotWeek
        fields = ('rank','skill_gunnery', 'skill_piloting', 'start_character_points')

    
        
class PilotTrainingForm(ModelForm):
    discipline = ModelChoiceField(queryset=PilotTraitGroup.objects.filter(discipline_type='T'))
    
    class Meta:
        model = models.PilotWeekTraits
        fields = ('discipline', 'trait', 'notes')        

PilotInlineSkillsForm = inlineformset_factory(models.PilotWeek, models.PilotWeekTraits, form=PilotTrainingForm, extra=1 )
