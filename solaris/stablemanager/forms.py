from django.forms import CharField, ModelChoiceField, Form
from django.db.models import Max

from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotDiscipline
from solaris.stablemanager.models import Stable
from solaris.stablemanager.ledger.models import Ledger
from solaris.battlereport.models import BroadcastWeek


class StableRegistrationForm(Form):
    stable_name = CharField(label='Stable Name', required=True)
    house = ModelChoiceField(label='House', required=True, queryset=House.objects.all())
    discipline_1 = ModelChoiceField(label='Discipline 1', required=True, queryset=PilotDiscipline.objects.all())
    discipline_2 = ModelChoiceField(label='Discipline 2', required=True, queryset=PilotDiscipline.objects.all())
    
    def register_stable(self, user):
        house = House.objects.get(house=self.cleaned_data['house'])
        
        stable = Stable.objects.create(
            stable_name = self.cleaned_data['stable_name']
        ,   owner = user
        ,   house = house
        ,   reputation = 0
        ,   current_week = self.week
        )
                        
        stable.stable_disciplines.add( PilotDiscipline.objects.get(name=self.cleaned_data['discipline_1']) )
        stable.stable_disciplines.add( PilotDiscipline.objects.get(name=self.cleaned_data['discipline_2']) )
        
        Ledger.objects.create(
            stable = stable
        ,   week = self.week
        ,   opening_balance = 10000000
        )
        
        stable.save()    
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data
