from solaris.forms import SolarisForm
from django.forms import CharField, ModelChoiceField
from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotDiscipline


class StableRegistrationForm(SolarisForm):
    stable_name = CharField(label='Stable Name', required=True)
    house = ModelChoiceField(label='House', required=True, queryset=House.objects.all())
    discipline_1 = ModelChoiceField(label='Discipline 1', required=True, queryset=PilotDiscipline.objects.all())
    discipline_2 = ModelChoiceField(label='Discipline 2', required=True, queryset=PilotDiscipline.objects.all())
    
