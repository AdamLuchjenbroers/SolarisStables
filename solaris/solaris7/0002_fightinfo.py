# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields

from solaris.utilities.data.fightinfo import load_weightclass_csv, load_fightgroup_csv, load_fighttype_csv, load_fightcondition_csv, load_map_csv

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
    
def load_fightconditions(apps, schema_editor):
    fields = ['name', 'rules']
    FightCondition = apps.get_model('warbook', 'FightCondition')
    
    load_fightcondition_csv('data/warbook.fightcondition.csv', csvfields=fields, FightCondition=FightCondition)            

def clear_fightconditions(apps, schema_editor):
    FightCondition = apps.get_model('warbook', 'FightCondition')
    FightCondition.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('solaris7', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FightCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('rules', markitup.fields.MarkupField(no_rendered_field=True)),
                ('_rules_rendered', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'solaris7_fightconditions',
                'verbose_name': 'Fight Condition',
                'verbose_name_plural': 'Fight Conditions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FightGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'solaris7_fightgroup',
                'verbose_name': 'Fight Group',
                'verbose_name_plural': 'Fight Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FightType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('urlname', models.CharField(max_length=50)),
                ('blurb', models.CharField(max_length=255, blank=True)),
                ('rules', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('is_simulation', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('_rules_rendered', models.TextField(editable=False, blank=True)),
                ('group', models.ForeignKey(related_name='fights', to='solaris7.FightGroup')),
            ],
            options={
                'ordering': ['order', 'name'],
                'db_table': 'solaris7_fighttype',
                'verbose_name': 'Fight Type',
                'verbose_name_plural': 'Fight Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('special_rules', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('_special_rules_rendered', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'solaris7_map',
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('lower', models.IntegerField()),
                ('upper', models.IntegerField()),
                ('in_use', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['lower'],
                'db_table': 'solaris7_weightclass',
                'verbose_name': 'Weight Class',
                'verbose_name_plural': 'Weight Classes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='rosteredfight',
            name='conditions',
            field=models.ManyToManyField(to='solaris7.FightCondition', through='solaris7.RosteredFightCondition'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rosteredfight',
            name='fight_map',
            field=models.ForeignKey(to='solaris7.Map'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rosteredfight',
            name='fight_type',
            field=models.ForeignKey(to='solaris7.FightType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rosteredfight',
            name='weightclass',
            field=models.ForeignKey(blank=True, to='solaris7.WeightClass', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rosteredfightcondition',
            name='condition',
            field=models.ForeignKey(to='solaris7.FightCondition'),
            preserve_default=True,
        ),
        migrations.RunPython(load_weightclasses, reverse_code=clear_weightclasses),
        migrations.RunPython(load_fightgroups, reverse_code=clear_fightgroups),
        migrations.RunPython(load_fighttypes, reverse_code=clear_fighttypes),
        migrations.RunPython(load_maps, reverse_code=clear_maps),
        migrations.RunPython(load_fightconditions, reverse_code=clear_fightconditions),
    ]
