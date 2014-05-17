from csv import DictReader
from django.forms import ModelForm
from solaris.warbook.equipment.models import Equipment

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment


fh = open('/home/notavi/Programming/SourceData/EquipmentCSV/DataLoad1.csv','r')

reader = DictReader(fh)

for row in reader:
    for boolean_field in ('splittable', 'crittable'):
        row[boolean_field] = (row[boolean_field] == 'TRUE')
    
    eq = EquipmentForm(row)
    if eq.is_valid():
        eq.save()
    