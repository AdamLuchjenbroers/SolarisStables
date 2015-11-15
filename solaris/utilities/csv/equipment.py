from csv import DictReader, DictWriter
from django.forms import ModelForm
from django.forms.models import model_to_dict

from solaris.warbook.equipment.models import Equipment

equipment_fields = ['id', 'name', 'ssw_name', 'equipment_class'
                   , 'tonnage_func', 'tonnage_factor', 'critical_func', 'critical_factor'
                   , 'cost_func', 'cost_factor', 'weapon_properties', 'basic_ammo'
                   , 'ammo_for', 'has_ammo', 'ammo_size', 'splittable', 'crittable'
                   , 'evaluate_last', 'record_status', 'fcs_artemis_iv', 'fcs_artemis_v'
                   , 'fcs_apollo' ]

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = equipment_fields

def getLauncher(launcher):
    try:
        ammo_for = Equipment.objects.get(id=int(launcher))
        return ammo_for
    except (Equipment.DoesNotExist, ValueError):
        pass
    
    try:
        ammo_for = Equipment.objects.get(name=launcher)
        return ammo_for
    except Equipment.DoesNotExist:
        pass   
    
    try:
        ammo_for = Equipment.objects.get(ssw_name=launcher)
        return ammo_for
    except Equipment.DoesNotExist:
        pass

def loadEquipmentCSV(csvfile):
    fh = open(csvfile,'r')
    
    reader = DictReader(fh)
    
    for row in reader:
        if 'name' not in row:
            row['name'] = row['ssw_name'].split(' - ')[1]
            
        if 'ammo_for' in row:
            launcher = getLauncher(row['ammo_for'])
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
            print '%s %s' % ('Loaded' if eq_instance == None else 'Updated', row['ssw_name'])
            eq.save()
            
    fh.close()

def dumpEquipmentCSV(csvfile, **kwargs):
    fh = open(csvfile,'w')

    to_fill = Equipment.objects.filter(**kwargs)

    writer = DictWriter(fh, fieldnames=equipment_fields)   
    writer.writeheader()
    
    for item in to_fill:
        writer.writerow( model_to_dict(item) )
        
    print "%i Equipment Items exported" % len(to_fill)
        
    fh.close()