from django.forms import ModelMultipleChoiceField, ModelForm
from django.db.models import Max

from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.stablemanager.models import Stable
from solaris.campaign.models import BroadcastWeek


class StableRegistrationForm(ModelForm):

    stable_disciplines = ModelMultipleChoiceField(label='Disciplines', required=True, queryset=PilotTraitGroup.objects.filter(discipline_type='T'))
    
    def __init__(self, **kwargs):
        super(StableRegistrationForm, self).__init__(**kwargs)  
        
        self.fields['stable_name'].label = 'Name'
        self.fields['house'].label = 'House'
        self.fields['stable_disciplines'].label = 'Disciplines'    
        self.fields['stable_disciplines'].classname = 'select_discipline'
 
    class Meta:
        model = Stable
        fields = ('stable_name', 'house', 'stable_disciplines')       
  
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data
