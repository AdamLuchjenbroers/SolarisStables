from django.forms import ModelChoiceField, ModelForm
from django.db.models import Max

from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.stablemanager.models import Stable
from solaris.campaign.models import BroadcastWeek


class StableRegistrationForm(ModelForm):

    discipline_1 = ModelChoiceField(label='Discipline 1', required=True, queryset=PilotTraitGroup.objects.all())
    discipline_2 = ModelChoiceField(label='Discipline 2', required=True, queryset=PilotTraitGroup.objects.all())
    
    def __init__(self, **kwargs):
        super(StableRegistrationForm, self).__init__(**kwargs)  
        
        self.fields['stable_name'].label = 'Name'
        self.fields['house'].label = 'House'    
 
    class Meta:
        model = Stable
        fields = ('stable_name', 'house', 'discipline_1', 'discipline_2')       
  
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data
