from csv import DictReader 
from django.conf import settings
from django.forms import ModelForm

from solaris.warbook.techtree.models import Technology
from solaris.warbook.equipment.models import Equipment

technology_fields = ['name', 'urlname', 'description', 'base_difficulty', 'tier', 'show']

def load_techtree_csv(csvfile, csvfields=technology_fields, Technology=Technology):
    csv_fh = open(csvfile,'r')
    reader = DictReader(csv_fh)

    class TechnologyForm(ModelForm):
        class Meta:
            model = Technology
            fields = csvfields
    
    loadcounts = { 'insert' : 0, 'update' : 0, 'failed': 0 }
    for row in reader:
        try:
            tech_instance = Technology.objects.get(name=row['name'])
        except Technology.DoesNotExist:
            tech_instance = None
            
        tech = TechnologyForm()
        if tech.is_valid():
            loadcounts['insert' if tech_instance == None else 'update'] += 1
            tech.save()
        else: 
            loadcounts['failed'] += 1
            print 'Failed to load: %s' % row['name']

    print 'Technology load complete: %i new, %i updated, %i failed to load' % (loadcounts['insert'], loadcounts['update'], loadcounts['failed'])           
    csv_fh.close()

def load_techtree_equipment_csv(csvfile, Equipment=Equipment, Technology=Technology):
    csv_fh = open(csvfile,'r')
    reader = DictReader(csv_fh)
    
    count = 0
    
    for row in reader:
        try:
            equip = Equipment.objects.get(ssw_name=row['ssw_name'])
            tech = Technology.objects.get(name=row['tech-name'])

            tech.access_to.add(equip)
            count += 1
        except Equipment.DoesNotExist:
            print "Unable to find Equipment '%s'" % row['ssw_name']
        except Technology.DoesNotExist:
            print "Unable to find Technology '%s'" % row['tech-name']

    print 'Loaded %i Technology - Equipment relationships' % count