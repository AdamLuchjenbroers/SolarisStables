from csv import DictReader 
from django.conf import settings

from solaris.warbook.techtree.models import Technology
from solaris.warbook.equipment.models import Equipment

def loadTechtreeEquipment(csvfile):
    csv_fh = open(csvfile,'r')
    reader = DictReader(csv_fh)

    for row in reader:
        try:
            equip = Equipment.objects.get(ssw_name=row['ssw_name'])
            tech = Technology.objects.get(name=row['tech-name'])

            tech.access_to.add(equip)
        except Equipment.DoesNotExist:
            print "Unable to find Equipment '%s'" % row['ssw_name']
        except Technology.DoesNotExist:
            print "Unable to find Technology '%s'" % row['tech-name']

