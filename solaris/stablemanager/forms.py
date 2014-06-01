from django.forms import HiddenInput, ModelChoiceField, ModelForm
from django.db.models import Max

from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotDiscipline
from solaris.stablemanager.models import Stable
from solaris.stablemanager.ledger.models import Ledger
from solaris.battlereport.models import BroadcastWeek


class StableRegistrationForm(ModelForm):

    discipline_1 = ModelChoiceField(label='Discipline 1', required=True, queryset=PilotDiscipline.objects.all())
    discipline_2 = ModelChoiceField(label='Discipline 2', required=True, queryset=PilotDiscipline.objects.all())
    
    def __init__(self, **kwargs):
        super(StableRegistrationForm, self).__init__(**kwargs)  
        
        self.fields['stable_name'].label = 'Name'
        self.fields['house'].label = 'House'    
 
    class Meta:
        model = Stable
        fields = ('stable_name', 'house', 'discipline_1', 'discipline_2')       
    
    def save(self, commit=True):
        super(StableRegistrationForm, self).save(commit=False)        
                    
        self.instance.stable_disciplines.add( PilotDiscipline.objects.get(name=self.cleaned_data['discipline_1']) )
        self.instance.stable_disciplines.add( PilotDiscipline.objects.get(name=self.cleaned_data['discipline_2']) )
        
        Ledger.objects.create(
            stable = self.instance
        ,   week = self.week
        ,   opening_balance = 10000000
        )        
        self.instance.save(commit=commit)    
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data
