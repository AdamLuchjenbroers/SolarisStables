# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0001_initial'),
        ('campaign', '0001_initial'),
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
                'db_table': 'solaris7_actiongroup',
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
                ('group', models.ForeignKey(related_name='actions', to='solaris7.ActionGroup')),
            ],
            options={
                'db_table': 'solaris7_actiontype',
                'verbose_name': 'Action Type',
                'verbose_name_plural': 'Action Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BroadcastWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_number', models.IntegerField()),
                ('week_started', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'solaris7_broadcastweek',
                'verbose_name': 'Broadcast Week',
            },
            bases=(models.Model,),
        ),
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
            name='RosteredFight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purse', models.IntegerField(null=True, blank=True)),
                ('group_tonnage', models.IntegerField(null=True, blank=True)),
                ('group_units', models.IntegerField(default=1)),
                ('fight_class', models.CharField(max_length=40, blank=True)),
                ('fought', models.BooleanField(default=False)),
                ('chassis', models.ForeignKey(blank=True, to='warbook.MechDesign', null=True)),
            ],
            options={
                'ordering': ['fight_type__order', 'group_units', 'weightclass__lower', 'group_tonnage'],
                'db_table': 'solaris7_rosteredfight',
                'verbose_name': 'Rostered Fight',
                'verbose_name_plural': 'Rostered Fights',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RosteredFightCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annotation', models.CharField(max_length=20, blank=True)),
                ('condition', models.ForeignKey(to='solaris7.FightCondition')),
                ('fight', models.ForeignKey(to='solaris7.RosteredFight')),
            ],
            options={
                'db_table': 'solaris7_fight_x_condition',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SolarisCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initial_balance', models.IntegerField()),
                ('actions_startweek', models.IntegerField(default=10)),
                ('actions_duringweek', models.IntegerField(default=10)),
                ('campaign', models.ForeignKey(to='campaign.Campaign')),
                ('initial_contracts', models.ManyToManyField(to='warbook.Technology')),
            ],
            options={
                'db_table': 'solaris7_campaign',
                'verbose_name': 'Solaris 7 Campaign',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StartingPilotTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('piloting', models.IntegerField()),
                ('gunnery', models.IntegerField()),
                ('fame', models.IntegerField(default=0)),
                ('campaign', models.ForeignKey(related_name='initial_pilots', to='solaris7.SolarisCampaign')),
                ('rank', models.ForeignKey(to='warbook.PilotRank')),
            ],
            options={
                'db_table': 'solaris7_pilottemplate',
                'verbose_name': 'Starting Pilot Template',
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
        migrations.CreateModel(
            name='Zodiac',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sign', models.CharField(max_length=20)),
                ('rules', models.TextField()),
                ('campaign', models.ForeignKey(blank=True, to='solaris7.SolarisCampaign', null=True)),
                ('next', models.OneToOneField(related_name='prev', null=True, to='solaris7.Zodiac')),
            ],
            options={
                'db_table': 'solaris7_zodiac',
                'verbose_name': 'Zodiac Sign',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='conditions',
            field=models.ManyToManyField(to='solaris7.FightCondition', through='solaris7.RosteredFightCondition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_map',
            field=models.ForeignKey(to='solaris7.Map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_type',
            field=models.ForeignKey(to='solaris7.FightType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='week',
            field=models.ForeignKey(related_name='fights', to='solaris7.BroadcastWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='weightclass',
            field=models.ForeignKey(blank=True, to='solaris7.WeightClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='broadcastweek',
            name='campaign',
            field=models.ForeignKey(related_name='weeks', to='solaris7.SolarisCampaign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='broadcastweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='solaris7.BroadcastWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='broadcastweek',
            name='sign',
            field=models.ForeignKey(to='solaris7.Zodiac'),
            preserve_default=True,
        ),
    ]
