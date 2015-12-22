from csv import DictReader 
from django.forms import ModelForm

from .csvtools import csv_import_to_model
from solaris.warbook.techtree.models import Technology
from solaris.warbook.equipment.models import Equipment

technology_fields = ['name', 'urlname', 'description', 'base_difficulty', 'tier', 'show']

def load_techtree_csv(csvfile, csvfields=technology_fields, Technology=Technology):
    csv_import_to_model(csvfile, Technology, csvfields, keyFields=('name',), booleanFields=('show',) )

def load_techtree_equipment_csv(csvfile, Equipment=Equipment, Technology=Technology):
    csv_fh = open(csvfile,'r')
    reader = DictReader(csv_fh)
    
    count = 0
    
    for row in reader:
        try:
            equip = Equipment.objects.get(ssw_name=row['ssw_name'])
            tech = Technology.objects.get(name=row['tech_name'])

            tech.access_to.add(equip)
            count += 1
        except Equipment.DoesNotExist:
            print "Unable to find Equipment '%s'" % row['ssw_name']
        except Technology.DoesNotExist:
            print "Unable to find Technology '%s'" % row['tech-name']

    print 'Loaded %i Technology - Equipment relationships' % count