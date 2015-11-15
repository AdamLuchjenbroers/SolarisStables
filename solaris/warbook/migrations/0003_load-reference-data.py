# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.equipment import loadEquipmentCSV
from solaris.utilities.data.mechs import loadMechFolder
from solaris.utilities.data.housemechs import matchFromListFile, createMatchingDict
        
def load_equipment(apps, schema_editor):
    loadEquipmentCSV('%s/data/warbook.equipment.csv' % settings.BASE_DIR);
    
def clear_equipment(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    Equipment.objects.all().delete()
    
def load_mechs(apps, schema_editor):
    loadMechFolder()
    
def clear_mechs(apps, schema_editor):
    MechDesign = apps.get_model('warbook', 'MechDesign')
    
    for mech in MechDesign.objects.all():
        # Clear equipment / mountings tables first before deleting.
        mech.reset_equipment()
        mech.delete()

productionLists = [
    ('House Liao', 'mechs.liao.txt'),
]
    
def load_productionlists():
    match_dict = createMatchingDict()
    
    for (house, filename) in productionLists:
        print "Loading mech list for %s [%s]" % (house, filename)
        full_path = '%s/%s' % (settings.BASE_DIR, filename)
        matchFromListFile(house, full_path, match_dict=match_dict, live=True)  
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0002_auto_20151113_1752'),
    ]

    operations = [
        migrations.RunPython(load_equipment, reverse_code=clear_equipment),
        migrations.RunPython(load_mechs, reverse_code=clear_equipment),
    ]
