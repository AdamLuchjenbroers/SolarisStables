#from django.forms.models import inlineformset_factory
from django import forms

from . import models
from snippets.widgets import SelectWithDisabled

from solaris.warbook.models import house_list_as_opttree
from solaris.warbook.pilotskill.models import PilotRank, PilotTrait, PilotTraitGroup

class PilotForm(forms.ModelForm):

    def __init__(self, querydict, stable=None, *args, **kwargs):
        super(PilotForm, self).__init__(querydict, *args, **kwargs)

        self.stable = stable
        self.fields['stable'].initial = stable.id
        self.fields['stable'].widget = forms.HiddenInput()

        self.fields['pilot_name'].label = 'Name (Optional):'
        self.fields['pilot_callsign'].label = 'Callsign:'

        self.fields['affiliation'].choices = (('', '-- Select House --'),) + house_list_as_opttree()
        self.fields['affiliation'].label = 'House or Faction:'
        self.fields['affiliation'].initial = stable.house

    def clean_callsign(self):
        callsign = self.cleaned_data['callsign']    
        return callsign.replace('/','-')

    def clean_stable(self):
        return self.stable

    class Meta:
        model = models.Pilot
        fields = ('stable', 'pilot_name', 'pilot_callsign','affiliation')

class AddPilotTraitAbstract(forms.ModelForm):
    class Meta:
        model = models.PilotWeekTraits
        fields = ('trait','notes', 'pilot_week')

    def __init__(self, *args, **kwargs):
        super(AddPilotTraitAbstract, self).__init__(*args, **kwargs)
        self.fields['notes'].label = 'Notes (Optional):'

    def get_choices(self, qset):
        choices = (("","-- Select Trait --"),)
        for group in qset:
            traitlist = tuple([ (trait.id, trait.name) for trait in group.traits.all()]) 
            choices += ((group.name, traitlist), )

        return choices

class AddPilotTraitForm(AddPilotTraitAbstract):
    def __init__(self, *args, **kwargs):
        super(AddPilotTraitForm, self).__init__(*args, **kwargs)
        self.fields['trait'].choices = self.get_choices(PilotTraitGroup.objects.exclude(discipline_type='T'))
        self.fields['trait'].label = 'Skill:'

PilotTraitFormSet = forms.inlineformset_factory(models.PilotWeek, models.PilotWeekTraits, form=AddPilotTraitForm, extra=0)

class AddPilotTrainingForm(AddPilotTraitAbstract):
    def __init__(self, *args, **kwargs):
        super(AddPilotTrainingForm, self).__init__(*args, **kwargs)
        self.fields['trait'].choices = self.get_choices(PilotTraitGroup.objects.filter(discipline_type='T'))
        self.fields['trait'].label = 'Problem:'

PilotTrainingFormSet = forms.inlineformset_factory(models.PilotWeek, models.PilotWeekTraits, form=AddPilotTrainingForm, extra=0)
        
class PilotWeekForm(forms.ModelForm):
    remove_choices = (('keep', 'Don\'t Remove'), ('remove', 'Remove from Stable'),) 
    remove = forms.ChoiceField(widget=forms.RadioSelect, initial='keep', choices=remove_choices)

    def __init__(self, *args, **kwargs):
        super(PilotWeekForm, self).__init__(*args, **kwargs)
        
        self.fields['start_character_points'].label = 'Experience:'
        self.fields['rank'].label = 'Ranking:'
        self.fields['rank'].initial = PilotRank.objects.get(rank='Rookie') 

        self.fields['skill_gunnery'].label = 'Gunnery:'
        self.fields['skill_piloting'].label = 'Piloting:'

        if self.instance != None and self.instance.is_locked():
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = models.PilotWeek
        fields = ('rank', 'rank_set', 'skill_gunnery', 'skill_piloting', 'start_character_points')

    def clean(self):
        cleaned = super(PilotWeekForm, self).clean()

        if self.instance == None or self.instance.rank_set:
            cleaned['rank_set'] = True
        elif not hasattr(self.instance, 'rank'):
            cleaned['rank_set'] = True
        elif self.instance.rank != cleaned['rank']:
            cleaned['rank_set'] = True
        else:
            cleaned['rank_set'] = False

        return cleaned

class PilotNamingForm(forms.ModelForm):
    pilot_name = forms.CharField(required=False)

    class Meta:
        model = models.Pilot
        fields = ('pilot_name', 'pilot_callsign')

    def summary(self):
        sw = self.instance.stable.get_stableweek()
        pw = self.instance.weeks.get(week=sw)
        return '%s, %i/%i' % (pw.rank.rank, pw.skill_gunnery, pw.skill_piloting)

PilotNamingFormSet = forms.modelformset_factory(models.Pilot, form=PilotNamingForm, fields=('pilot_name', 'pilot_callsign'), extra=0)

class PilotActionForm(forms.Form):
    pilot = forms.ChoiceField(label='Pilot:', widget=SelectWithDisabled)

    def __init__(self, stableweek=None, *args, **kwargs):
        super(PilotActionForm, self).__init__(*args, **kwargs)

        pilots = [('','-- Select Pilot --'),]
        for pw in stableweek.pilots.all_living():
            pilots.append((pw.id, {'label' : pw.pilot.pilot_callsign, 'disabled': pw.is_locked()}))

        self.fields['pilot'].choices = pilots 
        
class PilotTrainingForm(PilotActionForm):
    training = forms.ChoiceField(label='Training:')
    skill = forms.ChoiceField(label='Skill:')
    notes = forms.CharField(max_length=50,label='Skill Notes (Optional):')
    
    def __init__(self, *args, **kwargs):
        super(PilotTrainingForm, self).__init__(*args, **kwargs)

        self.fields['training'].widget.attrs['disabled'] = True
        self.fields['skill'].widget.attrs['disabled'] = True
        self.fields['notes'].widget.attrs['disabled'] = True

class PilotTraitForm(PilotActionForm):
    trait = forms.ChoiceField(label="Problem:")
    notes = forms.CharField(label='Problem Notes (Optional):', max_length=50)

    def __init__(self, *args, **kwargs):
        super(PilotTraitForm, self).__init__(*args, **kwargs)
        
        choices = (("","-- Select Trait --"),)
        for group in PilotTraitGroup.objects.exclude(discipline_type='T'):
            traitlist = tuple([ (trait.id, trait.name) for trait in group.traits.all()]) 
            choices += ((group.name, traitlist), )

        self.fields['trait'].choices = choices

class PilotDefermentForm(PilotActionForm):
    pilot = forms.ChoiceField(label='Pilot:', widget=SelectWithDisabled)
    deferred = forms.ChoiceField(label='Deferred:')
    notes = forms.CharField(max_length=50, label='Notes (Optional):')
    duration = forms.IntegerField(label='Duration (in Weeks):')

    def __init__(self, stableweek=None, *args, **kwargs):
        super(PilotActionForm, self).__init__(*args, **kwargs)

        pilots = [('','-- Select Pilot --'),]
        for pw in stableweek.pilots.all_living():
            disabled = (pw.traits.exclude(trait__discipline__discipline_type='T').count() == 0)
            pilots.append((pw.id, {'label' : pw.pilot.pilot_callsign, 'disabled': disabled }))

        self.fields['pilot'] = forms.ChoiceField(choices=pilots, widget=SelectWithDisabled, label='Pilot:')

