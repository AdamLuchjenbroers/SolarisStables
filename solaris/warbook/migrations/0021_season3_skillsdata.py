# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.pilotskills import load_pilottraitgroup_csv, load_pilottrait_csv

def add_secondary_training_cost(apps, schema_editor):
    TrainingCost = apps.get_model('warbook', 'TrainingCost')
    costs = [
      {'training' : '2', 'train_from' : 0, 'train_to' : 1, 'cost' : 20}
    , {'training' : '2', 'train_from' : 1, 'train_to' : 2, 'cost' : 35}
    , {'training' : '2', 'train_from' : 2, 'train_to' : 3, 'cost' : 45}
    ]

    for record in costs:
        TrainingCost.objects.create(**record) 

def remove_secondary_training_cost(apps, schema_editor):
    TrainingCost = apps.get_model('warbook', 'TrainingCost')
    TrainingCost.objects.filter(training='2').delete()

def reload_trait_groups(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')
    fields = ['name', 'discipline_type', 'rank_restricted', 'urlname' ,'blurb']

    PilotTraitGroup.objects.all().delete()
    load_pilottraitgroup_csv('%s/data/warbook.pilottraitgroup.csv' % settings.BASE_DIR, csvfields=fields, PilotTraitGroup=PilotTraitGroup );
 
def reload_traits(apps, schema_editor):
    PilotTrait = apps.get_model('warbook','PilotTrait')

    fields = ['discipline', 'table', 'item', 'bv_mod', 'name', 'description']

    PilotTrait.objects.all().delete()
    load_pilottrait_csv('%s/data/warbook.pilottrait.csv' % settings.BASE_DIR, csvfields=fields, PilotTrait=PilotTrait );

    
def noop(apps, schema_editor):
    # No Operation
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0020_season3_skills'),
    ]

    operations = [
        migrations.RunPython(add_secondary_training_cost, reverse_code=remove_secondary_training_cost),
        migrations.RunPython(reload_trait_groups, reverse_code=noop),
        migrations.RunPython(reload_traits, reverse_code=noop),
    ]
