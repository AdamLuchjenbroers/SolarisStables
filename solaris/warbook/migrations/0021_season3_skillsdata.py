# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from csv import DictReader

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.csvtools import csv_import_to_model, migration_map_fk
from solaris.utilities.data.pilotskills import load_pilottraitgroup_csv, load_pilottrait_csv
from solaris.utilities.data.houses import load_house_csv

def load_action_groups(apps, schema_editor):
    ActionGroup = apps.get_model('warbook', 'ActionGroup')
    ActionGroup.objects.all().delete()

    csv_import_to_model('data/warbook.actiongroups.csv'
                       , ActionGroup, ['group','start_only']
                       , booleanFields=['start_only',]
                       , keyFields=['group',]
                       )

def load_action_types(apps, schema_editor):
    ActionType = apps.get_model('warbook', 'ActionType')
    ActionType.objects.all().delete()


    csv_import_to_model('data/warbook.actiontypes.csv'
                       , ActionType
                       , ['group', 'action', 'base_cost', 'base_cost_max', 'description', 'max_per_week']
                       , keyFields=['action','group']
                       , mapFunctions={'group': migration_map_fk(apps, 'warbook', 'ActionGroup', 'group')} 
                       )

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

def add_rank_skill_info(apps, schema_editor):
    PilotRank = apps.get_model('warbook','PilotRank')
    skill_info = [
      {'rank' : 'Champion', 'secondary_skills_limit' : 3, 'restricted_skills' : True} 
    , {'rank' : 'Star', 'secondary_skills_limit' : 2, 'restricted_skills' : True} 
    , {'rank' : 'Contender', 'secondary_skills_limit' : 1, 'restricted_skills' : False} 
    , {'rank' : 'Rookie', 'secondary_skills_limit' : 1, 'restricted_skills' : False} 
    ]

    for row in skill_info:
        rank = PilotRank.objects.get(rank=row['rank'])

        rank.secondary_skills_limit = row['secondary_skills_limit']
        rank.restricted_skills = row['restricted_skills']
        rank.save()

def update_house_info(apps, schema_editor):
    fields = ['house', 'blurb', 'stable_valid', 'selectable_disciplines'] 
    House = apps.get_model('warbook', 'House')
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')

    load_house_csv('data/warbook.house.csv', csvfields=fields, House=House, PilotTraitGroup=PilotTraitGroup)

def reload_trait_groups(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')
 
    # Stash a list of stable disciplines so we can restore them after reloading the table.
    Stable = apps.get_model('stablemanager', 'Stable')

    stable_disciplines = dict()
    for s in Stable.objects.all():
        discipline_list = (discipline.name for discipline in s.stable_disciplines.all())
        stable_disciplines[s] = discipline_list

        # Clear the list to avoid primary key issues.
        s.stable_disciplines.all().delete()

    fields = ['name', 'discipline_type', 'rank_restricted', 'urlname' ,'blurb']

    PilotTraitGroup.objects.all().delete()
    load_pilottraitgroup_csv('%s/data/warbook.pilottraitgroup.csv' % settings.BASE_DIR, csvfields=fields, PilotTraitGroup=PilotTraitGroup );

    # Restore Disciplines list.
    for stable, discipline_list in stable_disciplines.items():
        for discipline in discipline_list:
            discipline_group = PilotTraitGroup.objects.get(name=discipline)
            stable.stable_disciplines.add(discipline_group)
 
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
        ('stablemanager', '0028_asset_count_details'),
    ]

    operations = [
        migrations.RunPython(add_secondary_training_cost, reverse_code=remove_secondary_training_cost),
        migrations.RunPython(reload_trait_groups, reverse_code=noop),
        migrations.RunPython(reload_traits, reverse_code=noop),
        migrations.RunPython(update_house_info, reverse_code=noop),
        migrations.RunPython(add_rank_skill_info, reverse_code=noop),
        migrations.RunPython(load_action_groups, reverse_code=noop),
        migrations.RunPython(load_action_types, reverse_code=noop),
    ]
