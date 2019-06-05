from csv import DictReader
from django.forms import ModelForm

from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotTraitGroup

from .csvtools import print_form_errors, handle_booleans, instance_for_row
    
house_fields = ['house', 'blurb', 'stable_valid', 'selectable_disciplines']

def load_house_csv(csvfile, csvfields=house_fields, House=House, PilotTraitGroup=PilotTraitGroup):
    fh = open(csvfile, 'r')

    class HouseForm(ModelForm):
        class Meta:
            model = House
            fields = csvfields

    reader = DictReader(fh)
    loadcounts = { 'insert' : 0, 'update' : 0, 'failed': 0 }

    for row in reader:
        handle_booleans(row, ('stable_valid',))

        discipline_list = [row.pop(column) for column in ('discipline_1', 'discipline_2', 'discipline_3')]
      
        house = instance_for_row(row, House, ('house',))
        house_form = HouseForm(row, instance=house) 

        if house_form.is_valid():
            loadcounts['insert' if house == None else 'update'] += 1
            house_form.save()

            house = house_form.instance
            house.house_disciplines.clear()
            for discipline in discipline_list:
                try:
                    ptg = PilotTraitGroup.objects.get(name=discipline)

                    house.house_disciplines.add(ptg)
                except PilotTraitGroup.DoesNotExist:
                    print "Could not find Discipline %s for House %s\n" % (discipline, house.house)
        else:
            loadcounts['failed'] += 1
            print 'Failed to load: %s' % row['house']
            print_form_errors(house_form)

    print 'Houses load complete: %i new, %i updated, %i failed to load' % (loadcounts['insert'], loadcounts['update'], loadcounts['failed'])           
    fh.close()

            
