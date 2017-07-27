# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '__first__'),
        ('campaign', '0006_track_week_start'),
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
                'db_table': 'campaign_conditions',
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
            ],
            options={
                'db_table': 'campaign_fightgroup',
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
                ('rules', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('is_simulation', models.BooleanField(default=False)),
                ('_rules_rendered', models.TextField(editable=False, blank=True)),
                ('group', models.ForeignKey(to='campaign.FightGroup')),
            ],
            options={
                'db_table': 'campaign_fighttype',
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
                'db_table': 'campaign_map',
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RosteredFight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fought', models.BooleanField(default=False)),
                ('conditions', models.ManyToManyField(to='campaign.FightCondition', through='roster.RosteredFightCondition')),
                ('fight_type', models.ForeignKey(to='campaign.FightType')),
                ('week', models.ForeignKey(related_name='fights', to='campaign.BroadcastWeek')),
            ],
            options={
                'db_table': 'campaign_rosteredfight',
                'verbose_name': 'Rostered Fight',
                'verbose_name_plural': 'Rostered Fights',
            },
            bases=(models.Model,),
        ),
    ]
