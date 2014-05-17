from csv import DictWriter
from django.forms.models import model_to_dict

from solaris.warbook.equipment.models import Equipment

fh = open('/home/notavi/Programming/SourceData/EquipmentCSV/DataLoad2.csv','w')

to_fill = Equipment.objects.filter(record_status=0)
header = model_to_dict(to_fill[0]).keys()

writer = DictWriter(fh, fieldnames=header)
writer.writeheader()

for item in to_fill:
    writer.writerow( model_to_dict(item) )