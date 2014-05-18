from csv import DictWriter
from django.forms.models import model_to_dict

from solaris.warbook.equipment.models import Equipment

fh = open('/home/notavi/Programming/SourceData/EquipmentCSV/DataLoad3.csv','w')

to_fill = Equipment.objects.filter(record_status=0)
header = ['id', 'name', 'ssw_name', 'equipment_class'
        , 'tonnage_func', 'tonnage_factor', 'critical_func', 'critical_factor', 'cost_func', 'cost_factor', 'weapon_properties'
        , 'basic_ammo', 'ammo_for', 'has_ammo', 'ammo_size', 'splittable', 'crittable', 'evaluate_last', 'record_status' ]

writer = DictWriter(fh, fieldnames=header)
print header

writer.writeheader()

for item in to_fill:
    writer.writerow( model_to_dict(item) )