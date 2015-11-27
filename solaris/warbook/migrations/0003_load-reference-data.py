# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.equipment import loadEquipmentCSV
 
def load_equipment(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    fields = ['id', 'name', 'ssw_name', 'equipment_class'
             , 'tonnage_func', 'tonnage_factor', 'critical_func', 'critical_factor'
             , 'cost_func', 'cost_factor', 'weapon_properties', 'basic_ammo'
             , 'ammo_for', 'has_ammo', 'ammo_size', 'splittable', 'crittable'
             , 'evaluate_last', 'record_status', 'fcs_artemis_iv', 'fcs_artemis_v'
             , 'fcs_apollo' ]

    loadEquipmentCSV('%s/data/excluded/warbook.equipment.csv' % settings.BASE_DIR, csvfields=fields, Equipment=Equipment );
    
def clear_equipment(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    Equipment.objects.all().delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0002_auto_20151113_1752'),
    ]

    operations = [
        migrations.RunPython(load_equipment, reverse_code=clear_equipment),
    ]
