from django.forms import ModelChoiceField, ModelMultipleChoiceField, ModelForm, ValidationError
from django.db.models import Max

from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.stablemanager.models import Stable
from solaris.campaign.solaris7.models import BroadcastWeek
from solaris.warbook.models import House, house_list_as_opttree

class StableRegistrationForm(ModelForm):
    stable_disciplines = ModelMultipleChoiceField(label='Disciplines', required=True, queryset=PilotTraitGroup.objects.filter(discipline_type='T', rank_restricted=False))
    
    def __init__(self, **kwargs):
        super(StableRegistrationForm, self).__init__(**kwargs)  
        
        self.fields['stable_name'].label = 'Name'
        self.fields['house'].label = 'House'
        self.fields['house'].choices = house_list_as_opttree()
        self.fields['stable_disciplines'].label = 'Disciplines'    
        self.fields['stable_disciplines'].classname = 'select_discipline'
 
    class Meta:
        model = Stable
        fields = ('stable_name', 'house', 'stable_disciplines')       

    def clean_house(self):
        name = self.cleaned_data['house']
        try:
            self.house = House.objects.get(house=name) 
        except House.DoesNotExist:
            raise ValidationError('House Name %s is unrecognised' % name)

        return name
    
    def clean(self):
        super(StableRegistrationForm,self).clean()
        if 'stable_disciplines' not in self.cleaned_data:
            raise ValidationError('No Disciplines have been selected')
        
        if len(self.cleaned_data['stable_disciplines']) != self.house.selectable_disciplines:
            raise ValidationError('%s should have %i selected disciplines, received %i.' 
                % (self.house.house, self.house.selectable_disciplines, len(self.cleaned_data['stable_disciplines'])))
        aggr = BroadcastWeek.objects.aggregate(Max('week_number'))
        self.week = BroadcastWeek.objects.get(week_number=aggr['week_number__max'])
        
        return self.cleaned_data
