from csv import DictReader
from django.forms import ModelForm
from solaris.warbook.equipment.models import Equipment



class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment

def get_launcher(launcher):
    try:
        ammo_for = Equipment.objects.get(id=int(row['ammo_for']))
        return ammo_for
    except (Equipment.DoesNotExist, ValueError):
        pass
    
    try:
        ammo_for = Equipment.objects.get(name=row['ammo_for'])
        return ammo_for
    except Equipment.DoesNotExist:
        pass   
    
    try:
        ammo_for = Equipment.objects.get(ssw_name=row['ammo_for'])
        return ammo_for
    except Equipment.DoesNotExist:
        pass

fh = open('/home/notavi/Programming/SourceData/EquipmentCSV/Actuators.csv','r')

reader = DictReader(fh)

for row in reader:
    if 'name' not in row:
        row['name'] = row['ssw_name'].split(' - ')[1]
        
    if 'ammo_for' in row:
        launcher = get_launcher(row['ammo_for'])
        if launcher:
            row['ammo_for'] = launcher.id
        
    try:
        eq_instance = Equipment.objects.get(ssw_name=row['ssw_name'])
    except Equipment.DoesNotExist:
        eq_instance = None
        
    for boolean_field in ('splittable', 'crittable'):
        row[boolean_field] = (row[boolean_field] == 'TRUE')
    
    eq = EquipmentForm(row, instance=eq_instance)
    if eq.is_valid():
        print 'Loaded %s' % row['ssw_name']
        eq.save()
