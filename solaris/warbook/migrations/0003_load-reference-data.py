# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from markitup.fields import MarkupField

from solaris.utilities.data.equipment import load_equipment_csv
from solaris.utilities.data.techtree import load_techtree_csv, load_techtree_equipment_csv
 
def clear_model(apps, appName, model):
    model = apps.get_model(appName, model)
    model.objects.all().delete()
    
def clear_equipment(apps, schema_editor):
    clear_model(apps,'warbook','equipment')
    
def clear_techtree(apps, schema_editor):
    clear_model(apps,'warbook','technology')
 
def load_equipment(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    fields = ['id', 'name', 'ssw_name', 'equipment_class'
             , 'tonnage_func', 'tonnage_factor', 'critical_func', 'critical_factor'
             , 'cost_func', 'cost_factor', 'weapon_properties', 'basic_ammo'
             , 'ammo_for', 'has_ammo', 'ammo_size', 'splittable', 'crittable'
             , 'evaluate_last', 'record_status', 'fcs_artemis_iv', 'fcs_artemis_v'
             , 'fcs_apollo' ]

    load_equipment_csv('%s/data/excluded/warbook.equipment.csv' % settings.BASE_DIR, csvfields=fields, Equipment=Equipment );

def load_techtree(apps, schema_editor):
    # Clean up any old entries
    clear_techtree(apps, schema_editor)
    
    Technology = apps.get_model('warbook','Technology')    
    fields = ['name', 'urlname', 'description', 'base_difficulty', 'tier', 'show']
    load_techtree_csv('%s/data/warbook.technology.csv' % settings.BASE_DIR, csvfields=fields, Technology=Technology)
    
def load_tech_x_equipment(apps, schema_editor):
    load_techtree_equipment_csv( '%s/data/warbook.techequipment.csv' % settings.BASE_DIR
                               , Technology=apps.get_model('warbook','technology')                            
                               , Equipment=apps.get_model('warbook','equipment') 
                               )
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0002_auto_20151113_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='cost_func',
            field=models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Cost'), (b'per_ton', b'Per Ton'), (b'structure', b'Structure'), (b'engine', b'Engine'), (b'gyro', b'Gyro'), (b'mech', b'Mech Tonnage'), (b'jumpjet', b'Jumpjet'), (b'per_er', b'By Engine Rating'), (b'masc', b'MASC'), (b'retract', b'Retractable Blade'), (b'per_leg', b'Per Leg')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='tonnage_func',
            field=models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Tonnage'), (b'jumpjet', b'Jumpjet'), (b'masc', b'MASC'), (b'melee', b'Melee Weapon'), (b'fraction', b'Fraction of Unit Tonnage'), (b'armour', b'Armour'), (b'engine', b'Engine'), (b'gyro', b'Gyro'), (b'structure', b'Internal Structure'), (b'targetting_computer', b'Targetting Computer'), (b'supercharger', b'Supercharger'), (b'retractable', b'Retractable Blade'), (b'turret', b'Mech Turret')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='critical_func',
            field=models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Criticals'), (b'masc', b'MASC'), (b'melee', b'Melee Weapon'), (b'targetting_computer', b'Targetting Computer'), (b'retractable', b'Retractable Blade'), (b'by_class', b'By Weight Class')]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='technology',
            name='category',
        ),
        migrations.AddField(
            model_name='technology',
            name='_description_rendered',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='technology',
            name='description',
            field=MarkupField(no_rendered_field=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='technology',
            name='tier',
            field=models.IntegerField(default=3, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental')]),
            preserve_default=True,
        ),
        migrations.RunPython(load_equipment, reverse_code=clear_equipment),
        migrations.RunPython(load_techtree, reverse_code=clear_techtree),
        migrations.RunPython(load_tech_x_equipment, reverse_code=noop),
    ]
