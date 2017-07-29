# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0019_actiontype_groupfix'),
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
                'db_table': 'warbook_fightconditions',
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
                'db_table': 'warbook_fightgroup',
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
                ('blurb', models.CharField(max_length=255, blank=True)),
                ('rules', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('is_simulation', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('_rules_rendered', models.TextField(editable=False, blank=True)),
                ('group', models.ForeignKey(to='warbook.FightGroup')),
            ],
            options={
                'ordering': ['order', 'name'],
                'db_table': 'warbook_fighttype',
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
                'db_table': 'warbook_map',
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
            bases=(models.Model,),
        ),
    ]
