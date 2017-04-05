# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields

from solaris.utilities.data.csvtools import csv_import_to_model, migration_map_fk

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
        ('warbook', '0017_pilotrank_receive_honours'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=50)),
                ('description', markitup.fields.MarkupField(no_rendered_field=True)),
                ('start_only', models.BooleanField(default=True)),
                ('_description_rendered', models.TextField(editable=False, blank=True)),
            ],
            options={
                'db_table': 'warbook_actiongroup',
                'verbose_name': 'Action Group',
                'verbose_name_plural': 'Action Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=50)),
                ('description', markitup.fields.MarkupField(no_rendered_field=True)),
                ('base_cost', models.IntegerField(default=1)),
                ('base_cost_max', models.IntegerField(default=None, null=True, blank=True)),
                ('max_per_week', models.IntegerField(default=1, null=True, blank=True)),
                ('_description_rendered', models.TextField(editable=False, blank=True)),
                ('group', models.ForeignKey(to='warbook.ActionGroup')),
            ],
            options={
                'db_table': 'warbook_actiontype',
                'verbose_name': 'Action Type',
                'verbose_name_plural': 'Action Types',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(load_action_groups, reverse_code=noop),
        migrations.RunPython(load_action_types, reverse_code=noop),
    ]
