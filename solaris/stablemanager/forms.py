from solaris.forms import SolarisForm
from django.forms import CharField, ModelChoiceField
from django.db.models import Max
from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotDiscipline
from solaris.stablemanager.models import Stable
from solaris.battlereport.models import BroadcastWeek


class StableRegistrationForm(SolarisForm):
    stable_name = CharField(label='Stable Name', required=True)
    house = ModelChoiceField(label='House', required=True, queryset=House.objects.all())
    discipline_1 = ModelChoiceField(label='Discipline 1', required=True, queryset=PilotDiscipline.objects.all())
    discipline_2 = ModelChoiceField(label='Discipline 2', required=True, queryset=PilotDiscipline.objects.all())
    
    def register_stable(self, user):
        print self.cleaned_data
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
        
        stable.save()    
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data