# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.csv.equipment import loadEquipmentCSV
from solaris.utilities.csv.mechs import loadMechFolder
        
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
