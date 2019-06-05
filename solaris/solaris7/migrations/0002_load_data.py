# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command

from solaris.utilities.data.csvtools import csv_import_to_model, migration_map_fk
from solaris.utilities.data.fightinfo import load_weightclass_csv, load_fightgroup_csv, load_fighttype_csv, load_fightcondition_csv, load_map_csv


def setup_campaign(apps, schema_editor):
    Campaign = apps.get_model('campaign', 'Campaign')
    masterCampaign = Campaign.objects.create(name='Solaris7', urlname='s7test')

    SolarisCampaign = apps.get_model('solaris7', 'SolarisCampaign')
    solarisCampaign = SolarisCampaign.objects.create(campaign=masterCampaign, initial_balance=75000000)
    
    Technology = apps.get_model('warbook', 'Technology')
    # Initial techtree is all Green + White techs
    for tech in Technology.objects.filter(tier__lte=1):
        solarisCampaign.initial_contracts.add(tech)

    solarisCampaign.save()

def load_zodiac(apps, schema_editor):
    Zodiac = apps.get_model('solaris7','Zodiac')
    signs = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Sheep', 'Monkey', 'Rooster', 'Dog', 'Pig']
    last = None

    SolarisCampaign = apps.get_model('solaris7', 'SolarisCampaign')
    sol = SolarisCampaign.objects.first()

    signs.reverse()
    for s in signs:
        last = Zodiac.objects.create(sign=s, rules='TBA', next=last, campaign=sol)
    
    pig = Zodiac.objects.get(sign='Pig')
    pig.next = Zodiac.objects.get(sign='Rat')
    pig.save()

def create_initial_week(apps, schema_editor):
    BroadcastWeek = apps.get_model('solaris7','BroadcastWeek')
    Zodiac = apps.get_model('solaris7','Zodiac')

    SolarisCampaign = apps.get_model('solaris7', 'SolarisCampaign')
    sol = SolarisCampaign.objects.first()

    BroadcastWeek.objects.create(week_number=1, campaign=sol, sign=Zodiac.objects.get(sign="Rat"))

def populate_templates(apps, schema_editor):
    StartingPilotTemplate = apps.get_model('solaris7','StartingPilotTemplate')
    SolarisCampaign = apps.get_model('solaris7', 'SolarisCampaign')
    PilotRank = apps.get_model('warbook', 'PilotRank')

    templates = [
       ('Champion' , 1, 3, 4),
       ('Star'     , 4, 4, 5),
       ('Contender', 3, 5, 6),
       ('Rookie'   , 3, 5, 6),
    ]
    
    for c in SolarisCampaign.objects.all():
        for (rank, count, gunnery, piloting) in templates:
            spt = StartingPilotTemplate.objects.create(
                campaign = c
            ,   rank = PilotRank.objects.get(rank=rank)
            ,   count = count
            ,   gunnery = gunnery
            ,   piloting = piloting
            )

def load_action_groups(apps, schema_editor):
    ActionGroup = apps.get_model('solaris7', 'ActionGroup')

    csv_import_to_model('data/warbook.actiongroups.csv'
                       , ActionGroup, ['group','start_only']
                       , booleanFields=['start_only',]
                       , keyFields=['group',]
                       )

def load_action_types(apps, schema_editor):
    ActionType = apps.get_model('solaris7', 'ActionType')

    csv_import_to_model('data/warbook.actiontypes.csv'
                       , ActionType
                       , ['group', 'action', 'base_cost', 'base_cost_max', 'description', 'max_per_week']
                       , keyFields=['action','group']
                       , mapFunctions={'group': migration_map_fk(apps, 'solaris7', 'ActionGroup', 'group')} 
                       )

def load_weightclasses(apps, schema_editor):
    fields = ['name', 'lower', 'upper']
    WeightClass = apps.get_model('solaris7', 'WeightClass')

    load_weightclass_csv('data/warbook.weightclass.csv', csvfields=fields, WeightClass=WeightClass)            

def clear_weightclasses(apps, schema_editor):
    WeightClass = apps.get_model('solaris7', 'WeightClass')
    WeightClass.objects.all().delete()
    
def load_fightgroups(apps, schema_editor):
    fields = ['name', 'order',]
    FightGroup = apps.get_model('solaris7', 'FightGroup')
    
    load_fightgroup_csv('data/warbook.fightgroup.csv', csvfields=fields, FightGroup=FightGroup)            

def clear_fightgroups(apps, schema_editor):
    FightGroup = apps.get_model('solaris7', 'FightGroup')
    FightGroup.objects.all().delete()
    
def load_fighttypes(apps, schema_editor):
    fields = ['group', 'name', 'order', 'urlname', 'blurb', 'rules', 'is_simulation']
    FightType = apps.get_model('solaris7', 'FightType')
    
    load_fighttype_csv('data/warbook.fighttype.csv', csvfields=fields, FightType=FightType)            

def clear_fighttypes(apps, schema_editor):
    FightType = apps.get_model('solaris7', 'FightType')
    FightType.objects.all().delete()
    
def load_maps(apps, schema_editor):
    fields = ['name', 'special_rules']
    Map = apps.get_model('solaris7', 'Map')
    
    load_map_csv('data/warbook.map.csv', csvfields=fields, Map=Map)            

def clear_maps(apps, schema_editor):
    Map = apps.get_model('solaris7', 'Map')
    Map.objects.all().delete()
    
def load_fightconditions(apps, schema_editor):
    fields = ['name', 'rules']
    FightCondition = apps.get_model('solaris7', 'FightCondition')
    
    load_fightcondition_csv('data/warbook.fightcondition.csv', csvfields=fields, FightCondition=FightCondition)            
def clear_fightconditions(apps, schema_editor):
    FightCondition = apps.get_model('solaris7', 'FightCondition')
    FightCondition.objects.all().delete()
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('solaris7', '0001_initial'),
        ('campaign', '0001_initial'),
        ('warbook', '0002_load_data'),
    ]

    operations = [
        migrations.RunPython(setup_campaign, reverse_code=noop),
        migrations.RunPython(load_zodiac, reverse_code=noop),
        migrations.RunPython(create_initial_week, reverse_code=noop),
        migrations.RunPython(populate_templates, reverse_code=noop),
        migrations.RunPython(load_action_groups, reverse_code=noop),
        migrations.RunPython(load_action_types, reverse_code=noop),
        migrations.RunPython(load_weightclasses, reverse_code=clear_weightclasses),
        migrations.RunPython(load_fightgroups, reverse_code=clear_fightgroups),
        migrations.RunPython(load_fighttypes, reverse_code=clear_fighttypes),
        migrations.RunPython(load_maps, reverse_code=clear_maps),
        migrations.RunPython(load_fightconditions, reverse_code=clear_fightconditions),
    ]
