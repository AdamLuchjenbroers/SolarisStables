# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.fightinfo import load_weightclass_csv, load_fightgroup_csv, load_fighttype_csv, load_map_csv

def load_weightclasses(apps, schema_editor):
    fields = ['name', 'lower', 'upper']
    WeightClass = apps.get_model('warbook', 'WeightClass')

    load_weightclass_csv('data/warbook.weightclass.csv', csvfields=fields, WeightClass=WeightClass)            

def clear_weightclasses(apps, schema_editor):
    WeightClass = apps.get_model('warbook', 'WeightClass')
    WeightClass.objects.all().delete()
    
def load_fightgroups(apps, schema_editor):
    fields = ['name', 'order',]
    FightGroup = apps.get_model('warbook', 'FightGroup')
    
    load_fightgroup_csv('data/warbook.fightgroup.csv', csvfields=fields, FightGroup=FightGroup)            

def clear_fightgroups(apps, schema_editor):
    FightGroup = apps.get_model('warbook', 'FightGroup')
    FightGroup.objects.all().delete()
    
def load_fighttypes(apps, schema_editor):
    fields = ['group', 'name', 'order', 'urlname', 'blurb', 'rules', 'is_simulation']
    FightType = apps.get_model('warbook', 'FightType')
    
    load_fighttype_csv('data/warbook.fighttype.csv', csvfields=fields, FightType=FightType)            

def clear_fighttypes(apps, schema_editor):
    FightType = apps.get_model('warbook', 'FightType')
    FightType.objects.all().delete()
    
def load_maps(apps, schema_editor):
    fields = ['name', 'special_rules']
    Map = apps.get_model('warbook', 'Map')
    
    load_map_csv('data/warbook.map.csv', csvfields=fields, Map=Map)            

def clear_maps(apps, schema_editor):
    Map = apps.get_model('warbook', 'Map')
    Map.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0023_weightclass'),
    ]

    operations = [
        migrations.RunPython(load_weightclasses, reverse_code=clear_weightclasses),
        migrations.RunPython(load_fightgroups, reverse_code=clear_fightgroups),
        migrations.RunPython(load_fighttypes, reverse_code=clear_fighttypes),
        migrations.RunPython(load_maps, reverse_code=clear_maps),
    ]
