from csv import DictReader, DictWriter
from django.forms import ModelForm
from django.forms.models import model_to_dict

from .csvtools import print_form_errors, handle_booleans, instance_for_row

equipment_fields = ['id', 'name', 'ssw_name', 'equipment_class'
                   , 'tonnage_func', 'tonnage_factor', 'critical_func', 'critical_factor'
                   , 'cost_func', 'cost_factor', 'weapon_properties', 'basic_ammo'
                   , 'ammo_for', 'has_ammo', 'ammo_size', 'splittable', 'crittable'
                   , 'evaluate_last', 'record_status', 'fcs_artemis_iv', 'fcs_artemis_v'
                   , 'fcs_apollo', 'tier' ]

from solaris.warbook.equipment.models import Equipment

def get_launcher(launcher, Equipment=Equipment):
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

def load_equipment_csv(csvfile, reassign_id=False, csvfields=equipment_fields, Equipment=Equipment):
    fh = open(csvfile,'r')

    class EquipmentForm(ModelForm):
        class Meta:
            model = Equipment
            fields = csvfields
    
    reader = DictReader(fh)
    loadcounts = { 'insert' : 0, 'update' : 0, 'failed': 0 }
    
    for row in reader:
        if 'name' not in row:
            row['name'] = row['ssw_name'].split(' - ')[1]
            
        if 'ammo_for' in row:
            launcher = get_launcher(row['ammo_for'], Equipment=Equipment)
            if launcher:
                row['ammo_for'] = launcher.id
            
        if 'id' in row and reassign_id:
            del row['id']
        
        boolFields = ('splittable', 'crittable', 'evaluate_last', 'basic_ammo'
                 , 'has_ammo', 'fcs_artemis_iv', 'fcs_artemis_v', 'fcs_apollo')
        handle_booleans(row, boolFields)
        
        eq_instance = instance_for_row(row, Equipment, ['ssw_name'])
        
        eq = EquipmentForm(row, instance=eq_instance)
        if eq.is_valid():
            loadcounts['insert' if eq_instance == None else 'update'] += 1
            eq.save()
        else: 
            loadcounts['failed'] += 1
            print 'Failed to load: %s' % row['ssw_name']
            print_form_errors(eq)

    print 'Equipment load complete: %i new, %i updated, %i failed to load' % (loadcounts['insert'], loadcounts['update'], loadcounts['failed'])           
    fh.close()

def dump_equipment_csv(csvfile, csvfields=equipment_fields, **kwargs):
    fh = open(csvfile,'w')

    to_fill = Equipment.objects.filter(**kwargs)

    writer = DictWriter(fh, fieldnames=csvfields)   
    writer.writeheader()
    
    for item in to_fill:
        writer.writerow( model_to_dict(item, fields=csvfields) )
        
    print "%i Equipment Items exported" % len(to_fill)
        
    fh.close()
