from django.forms.models import inlineformset_factory
from django.forms import Form, ModelForm, ChoiceField, ModelChoiceField, HiddenInput, CharField, modelformset_factory

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
        
class PilotTrainingForm(Form):
    pilot = ChoiceField()
    training = ChoiceField()
    skill = ChoiceField()
    notes = CharField(max_length=50)
    
    def __init__(self, stableweek=None, *args, **kwargs):
        super(PilotTrainingForm, self).__init__(*args, **kwargs)
        self.fields['pilot'].choices =[("",'--')] + [(pw.id, pw.pilot.pilot_callsign) for pw in stableweek.pilots.filter(wounds__lt=6)]

        self.fields['training'].widget.attrs['disabled'] = True
        self.fields['skill'].widget.attrs['disabled'] = True
        self.fields['notes'].widget.attrs['disabled'] = True


