# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command

from markitup.fields import MarkupField
import json

from solaris.utilities.data.equipment import load_equipment_csv
from solaris.utilities.data.techtree import load_techtree_csv, load_techtree_equipment_csv
from solaris.utilities.data.mechs import loadMechFolder
from solaris.utilities.data.housemechs import matchFromListFile, createMatchingDict
from solaris.utilities.data.csvtools import csv_import_to_model, migration_map_fk
from solaris.utilities.data.pilotskills import load_pilottraitgroup_csv, load_pilottrait_csv
from solaris.utilities.data.houses import load_house_csv

 
def clear_model(apps, appName, model):
    model = apps.get_model(appName, model)
    model.objects.all().delete()
    
def clear_equipment(apps, schema_editor):
    clear_model(apps,'warbook','equipment')
    
def clear_techtree(apps, schema_editor):
    clear_model(apps,'warbook','technology')
    
def load_pilottraitgroup(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')

    fields = ['name', 'discipline_type', 'rank_restricted', 'urlname' ,'blurb']
    load_pilottraitgroup_csv('%s/data/warbook.pilottraitgroup.csv' % settings.BASE_DIR, csvfields=fields, PilotTraitGroup=PilotTraitGroup );
 
def load_pilottrait(apps, schema_editor):
    PilotTrait = apps.get_model('warbook','PilotTrait')

    fields = ['discipline', 'table', 'item', 'bv_mod', 'name', 'description']

    PilotTrait.objects.all().delete()

def load_houses(apps, schema_editor):
    #FIXME: House loader should be re-written to load all from one .csv
    House = apps.get_model('warbook','House')   
    PilotTraitGroup = apps.get_model('warbook','PilotTraitGroup')   

    srcfile = open('data/warbook.house.json','r')
    house_json = srcfile.read()
    srcfile.close()

    data = json.loads(house_json)
    for row in data:
        ids = row['fields']['house_disciplines']
        del row['fields']['house_disciplines']

        house = House.objects.create(**row['fields']) 

        for discipline in PilotTraitGroup.objects.filter(id__in=ids):
            house.house_disciplines.add(discipline)

    fields = ['house', 'blurb', 'stable_valid', 'selectable_disciplines'] 
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')

    load_house_csv('data/warbook.house.csv', csvfields=fields, House=House, PilotTraitGroup=PilotTraitGroup)
 
  
def load_mechlocations(apps, schema_editor):
    call_command('loaddata', 'data/warbook.mechlocation.json');
         
def load_pilotranks(apps, schema_editor):
    call_command('loaddata', 'data/warbook.pilotrank.json');
    
def load_trainingcost(apps, schema_editor):
    call_command('loaddata', 'data/warbook.trainingcost.json');

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

def derive_equipment_tiers(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    for eq in Equipment.objects.all():
        eq.tier = eq.supplied_by.all().aggregate(models.Min('tier'))['tier__min']
        if eq.tier == None:
            eq.tier = 3
        eq.save()

def load_mechs(apps, schema_editor):
    loadMechFolder()
    
def clear_mechs(apps, schema_editor):
    MechDesign = apps.get_model('warbook', 'MechDesign')
    
    for mech in MechDesign.objects.all():
        # Clear equipment / mountings tables first before deleting.
        mech.reset_equipment()
        mech.delete()

productionLists = [
    ('House Liao'   , 'mechs.liao.txt'   ),
    ('House Kurita' , 'mechs.kurita.txt' ),
    ('House Davion' , 'mechs.davion.txt' ),
    ('House Steiner', 'mechs.steiner.txt'),
    ('House Marik'  , 'mechs.marik.txt'  ),
    ('ComStar'      , 'mechs.comstar.txt'),
]
    
def load_productionlists(apps, schema_editor):
    mech_class = apps.get_model('warbook', 'MechDesign')
    match_dict = createMatchingDict(MechDesign=mech_class)
    house_class = apps.get_model('warbook', 'House')
    
    for (house, filename) in productionLists:
        print "Loading mech list for %s [%s]" % (house, filename)
        full_path = '%s/data/excluded/%s' % (settings.BASE_DIR, filename)
        matchFromListFile(house, full_path, match_dict=match_dict, live=True, House=house_class)  

def derive_mech_tiers(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    MechDesign = apps.get_model('warbook','MechDesign')
    for mech in MechDesign.objects.all():
       mech_eq = Equipment.objects.filter(id__in=mech.loadout.all().values('equipment'))   
       mech.tier = mech_eq.aggregate(models.Max('tier'))['tier__max'] 
       mech.save() 

def load_action_groups(apps, schema_editor):
    ActionGroup = apps.get_model('warbook', 'ActionGroup')

    csv_import_to_model('data/warbook.actiongroups.csv'
                       , ActionGroup, ['group','start_only']
                       , booleanFields=['start_only',]
                       , keyFields=['group',]
                       )

def load_action_types(apps, schema_editor):
    ActionType = apps.get_model('warbook', 'ActionType')

    csv_import_to_model('data/warbook.actiontypes.csv'
                       , ActionType
                       , ['group', 'action', 'base_cost', 'base_cost_max', 'description', 'max_per_week']
                       , keyFields=['action','group']
                       , mapFunctions={'group': migration_map_fk(apps, 'warbook', 'ActionGroup', 'group')} 
                       )

def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_mechlocations, reverse_code=noop),
        migrations.RunPython(load_pilotranks, reverse_code=noop),
        migrations.RunPython(load_trainingcost, reverse_code=noop),
        migrations.RunPython(load_pilottraitgroup, reverse_code=noop),
        migrations.RunPython(load_pilottrait, reverse_code=noop),
        migrations.RunPython(load_houses, reverse_code=noop),
        migrations.RunPython(load_equipment, reverse_code=clear_equipment),
        migrations.RunPython(load_techtree, reverse_code=clear_techtree),
        migrations.RunPython(load_tech_x_equipment, reverse_code=noop),
        migrations.RunPython(derive_equipment_tiers, reverse_code=noop),
        migrations.RunPython(load_mechs, reverse_code=noop),
        migrations.RunPython(load_productionlists, reverse_code=noop),
        migrations.RunPython(derive_mech_tiers, reverse_code=noop),
        migrations.RunPython(load_action_groups, reverse_code=noop),
        migrations.RunPython(load_action_types, reverse_code=noop),
    ]
