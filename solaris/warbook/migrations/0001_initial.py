# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import models, migrations
from decimal import Decimal
from django.core.management import call_command

    
def load_houses(apps, schema_editor):
    call_command('loaddata', 'data/warbook.house.json');
  
def load_mechlocations(apps, schema_editor):
    from solaris.warbook.mech import refdata
    MechLocation = apps.get_model('warbook','MechLocation')   
 
    locations = {}
    for (code, name) in refdata.locations_all:
        locations[code] = MechLocation.objects.create (
                            location = code
                          , criticals = refdata.criticals(code)
                          )

    for (torso, rear) in [(loc, 'R'+loc) for loc in ('CT','LT','RT')]:
        locations[rear].rear_of = locations[torso]
        locations[rear].save()
         
def load_pilotranks(apps, schema_editor):
    call_command('loaddata', 'data/warbook.pilotrank.json');
    
def load_pilottraitgroup(apps, schema_editor):
    call_command('loaddata', 'data/warbook.pilottraitgroup.json');
    
def load_pilottrait(apps, schema_editor):
    call_command('loaddata', 'data/warbook.pilottrait.json');
        
def load_trainingcost(apps, schema_editor):
    call_command('loaddata', 'data/warbook.trainingcost.json');
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'FIXME', max_length=100)),
                ('ssw_name', models.CharField(unique=True, max_length=100)),
                ('tonnage_func', models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Tonnage'), (b'jumpjet', b'Jumpjet'), (b'masc', b'MASC'), (b'melee', b'Melee Weapon'), (b'armour', b'Armour'), (b'engine', b'Engine'), (b'gyro', b'Gyro'), (b'structure', b'Internal Structure'), (b'targetting_computer', b'Targetting Computer'), (b'supercharger', b'Supercharger'), (b'retractable', b'Retractable Blade')])),
                ('tonnage_factor', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('critical_func', models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Criticals'), (b'masc', b'MASC'), (b'melee', b'Melee Weapon'), (b'targetting_computer', b'Targetting Computer'), (b'retractable', b'Retractable Blade')])),
                ('critical_factor', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('cost_func', models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Cost'), (b'per_ton', b'Per Ton'), (b'engine', b'Engine'), (b'gyro', b'Gyro'), (b'mech', b'Mech Tonnage'), (b'jumpjet', b'Jumpjet'), (b'per_er', b'By Engine Rating')])),
                ('cost_factor', models.DecimalField(null=True, max_digits=16, decimal_places=4)),
                ('splittable', models.BooleanField(default=False)),
                ('crittable', models.BooleanField(default=True)),
                ('has_ammo', models.BooleanField(default=False)),
                ('basic_ammo', models.BooleanField(default=False)),
                ('ammo_size', models.IntegerField(null=True, blank=True)),
                ('weapon_properties', models.CharField(max_length=20, null=True, blank=True)),
                ('evaluate_last', models.BooleanField(default=False)),
                ('record_status', models.IntegerField(default=0, choices=[(0, b'Aggressive Load'), (1, b'Incomplete'), (2, b'Completed')])),
                ('equipment_class', models.CharField(default=b'?', max_length=1, choices=[(b'E', b'Engine'), (b'G', b'Gyro'), (b'C', b'Cockpit & Systems'), (b'W', b'Weapon'), (b'H', b'Heatsink'), (b'J', b'Jumpjet'), (b'Q', b'Equipment'), (b'S', b'Armour / Structure'), (b'A', b'Ammunition'), (b'T', b'Actuator'), (b'M', b'Mission Items'), (b'?', b'Unclassified')])),
                ('ammo_for', models.ForeignKey(blank=True, to='warbook.Equipment', null=True)),
            ],
            options={
                'ordering': ['equipment_class', 'name'],
                'db_table': 'warbook_equipment',
                'verbose_name': 'Equipment',
                'verbose_name_plural': 'Equipment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house', models.CharField(unique=True, max_length=20)),
                ('blurb', models.TextField()),
            ],
            options={
                'db_table': 'warbook_house',
                'verbose_name': 'House',
                'verbose_name_plural': 'Houses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MechDesign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mech_name', models.CharField(max_length=50)),
                ('mech_code', models.CharField(max_length=50)),
                ('omni_loadout', models.CharField(default=b'Base', max_length=30, blank=True)),
                ('stock_design', models.BooleanField(default=True)),
                ('credit_value', models.IntegerField(null=True)),
                ('bv_value', models.IntegerField(null=True)),
                ('tonnage', models.IntegerField()),
                ('engine_rating', models.IntegerField()),
                ('is_omni', models.BooleanField(default=False)),
                ('ssw_filename', models.CharField(max_length=1024, null=True, blank=True)),
                ('motive_type', models.CharField(max_length=1, choices=[(b'B', b'Biped'), (b'Q', b'Quad')])),
                ('tech_base', models.CharField(max_length=1, choices=[(b'I', b'Inner Sphere'), (b'C', b'Clan'), (b'M', b'Mixed')])),
                ('production_type', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Standard Production Design'), (b'H', b'Historical Custom Design'), (b'C', b'Customized Stable Design')])),
                ('omni_basechassis', models.ForeignKey(related_name='loadouts', blank=True, to='warbook.MechDesign', null=True)),
            ],
            options={
                'ordering': ['tonnage', 'mech_name', 'mech_code', 'omni_loadout'],
                'db_table': 'warbook_mechdesign',
                'verbose_name': 'Mech Design',
                'verbose_name_plural': 'Mech Designs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MechDesignLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('armour', models.IntegerField()),
                ('structure', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'warbook_mechdesignlocation',
                'verbose_name': 'Mech Design Location',
                'verbose_name_plural': 'Mech Design Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MechEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipment', models.ForeignKey(to='warbook.Equipment')),
                ('mech', models.ForeignKey(related_name='loadout', to='warbook.MechDesign')),
            ],
            options={
                'db_table': 'warbook_mechequipment',
                'verbose_name': 'Mech Equipment',
                'verbose_name_plural': 'Mech Equipment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MechLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(unique=True, max_length=3, choices=[(b'HD', b'Head'), (b'LT', b'Left Torso'), (b'RT', b'Right Torso'), (b'CT', b'Center Torso'), (b'RLT', b'Left Torso (Rear)'), (b'RRT', b'Right Torso (Rear)'), (b'RCT', b'Center Torso (Rear)'), (b'--', b'No Location'), (b'RFL', b'Right Fore Leg'), (b'RRL', b'Right Rear Leg'), (b'LFL', b'Left Fore Leg'), (b'LRL', b'Left Rear Leg'), (b'RA', b'Right Arm'), (b'LA', b'Left Arm'), (b'RL', b'Right Leg'), (b'LL', b'Left Leg')])),
                ('criticals', models.IntegerField()),
                ('rear_of', models.ForeignKey(to='warbook.MechLocation', null=True)),
            ],
            options={
                'db_table': 'warbook_mechlocation',
                'verbose_name': 'Mech Location',
                'verbose_name_plural': 'Mech Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mounting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slots', models.CharField(max_length=30, blank=True)),
                ('rear_firing', models.BooleanField(default=False)),
                ('turret_mounted', models.BooleanField(default=False)),
                ('equipment', models.ForeignKey(related_name='mountings', to='warbook.MechEquipment')),
                ('location', models.ForeignKey(related_name='criticals', to='warbook.MechDesignLocation')),
            ],
            options={
                'db_table': 'warbook_mechmounting',
                'verbose_name': 'Mounting',
                'verbose_name_plural': 'Mounting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.CharField(unique=True, max_length=20)),
                ('min_gunnery', models.IntegerField()),
                ('min_piloting', models.IntegerField()),
                ('skills_limit', models.IntegerField()),
                ('auto_train_cp', models.IntegerField(default=0)),
                ('promotion', models.ForeignKey(blank=True, to='warbook.PilotRank', null=True)),
            ],
            options={
                'db_table': 'warbook_pilotrank',
                'verbose_name': 'Pilot Rank',
                'verbose_name_plural': 'Pilot Ranks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotTrait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('bv_mod', models.DecimalField(max_digits=6, decimal_places=3, choices=[(Decimal('0.000'), b'No Modifier'), (Decimal('0.050'), b'Piloting Skill'), (Decimal('0.200'), b'Gunnery Skill')])),
            ],
            options={
                'db_table': 'warbook_pilottrait',
                'verbose_name': 'Pilot Trait',
                'verbose_name_plural': 'Pilot Traits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotTraitGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('blurb', models.TextField()),
                ('urlname', models.CharField(unique=True, max_length=20)),
                ('discipline_type', models.CharField(default=b'I', max_length=1, choices=[(b'T', b'Training'), (b'I', b'Issues'), (b'O', b'Other')])),
            ],
            options={
                'db_table': 'warbook_pilottraitgroup',
                'verbose_name': 'Pilot Trait Group',
                'verbose_name_plural': 'Pilot Trait Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('category', models.CharField(max_length=8, choices=[(b'weap', b'Weaponry'), (b'equip', b'Equipment'), (b'cons', b'Construction'), (b'ammo', b'Ammunition'), (b'phys', b'Physical Weapons')])),
                ('urlname', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('base_difficulty', models.IntegerField()),
                ('tier', models.IntegerField(choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental')])),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'warbook_technology',
                'verbose_name_plural': 'Technologies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TechnologyRollModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modifier', models.IntegerField(default=2)),
                ('condition', models.CharField(max_length=120)),
                ('technology', models.ForeignKey(related_name='modifiers', to='warbook.Technology')),
            ],
            options={
                'db_table': 'warbook_technologyrollmodifier',
                'verbose_name_plural': 'Technology Roll Modifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrainingCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('training', models.CharField(max_length=1, choices=[(b'P', b'Piloting'), (b'G', b'Gunnery'), (b'S', b'Skills')])),
                ('train_from', models.IntegerField()),
                ('train_to', models.IntegerField()),
                ('cost', models.IntegerField()),
            ],
            options={
                'db_table': 'warbook_trainingcost',
                'verbose_name': 'Training Cost',
                'verbose_name_plural': 'Training Costs',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='trainingcost',
            unique_together=set([('training', 'train_to')]),
        ),
        migrations.AddField(
            model_name='pilottrait',
            name='discipline',
            field=models.ForeignKey(related_name='traits', blank=True, to='warbook.PilotTraitGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mechdesignlocation',
            name='location',
            field=models.ForeignKey(to='warbook.MechLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mechdesignlocation',
            name='mech',
            field=models.ForeignKey(related_name='locations', to='warbook.MechDesign'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='mechdesignlocation',
            unique_together=set([('mech', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='mechdesign',
            unique_together=set([('ssw_filename', 'omni_loadout'), ('mech_name', 'mech_code', 'omni_loadout')]),
        ),
        migrations.AddField(
            model_name='house',
            name='house_disciplines',
            field=models.ManyToManyField(to='warbook.PilotTraitGroup', db_table=b'warbook_house_x_discipline'),
            preserve_default=True,
        ),
        migrations.RunPython(load_mechlocations, reverse_code=noop),
        migrations.RunPython(load_pilotranks, reverse_code=noop),
        migrations.RunPython(load_pilottraitgroup, reverse_code=noop),
        migrations.RunPython(load_pilottrait, reverse_code=noop),
        migrations.RunPython(load_trainingcost, reverse_code=noop),
        migrations.RunPython(load_houses, reverse_code=noop),
    ]
