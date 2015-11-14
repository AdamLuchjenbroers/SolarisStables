# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('warbook', '0002_auto_20151113_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=40)),
                ('cost', models.IntegerField()),
                ('type', models.CharField(max_length=1, choices=[(b'R', b'Repair Bill'), (b'P', b'Purchase'), (b'E', b'Other Expenses'), (b'W', b'Winnings'), (b'I', b'Other Income')])),
                ('tied', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'stablemanager_ledgeritem',
                'verbose_name': 'StableWeek Item',
                'verbose_name_plural': 'StableWeek Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pilot_name', models.CharField(max_length=50, blank=True)),
                ('pilot_callsign', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('affiliation', models.ForeignKey(to='warbook.House')),
            ],
            options={
                'db_table': 'stablemanager_pilot',
                'verbose_name': 'Pilot',
                'verbose_name_plural': 'Pilots',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotTrainingEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'stablemanager_trainingevent',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_character_points', models.IntegerField(default=0)),
                ('adjust_character_points', models.IntegerField(default=0)),
                ('assigned_training_points', models.IntegerField(default=0)),
                ('skill_gunnery', models.IntegerField(default=5)),
                ('skill_piloting', models.IntegerField(default=6)),
                ('wounds', models.IntegerField(default=0)),
                ('pilot', models.ForeignKey(related_name='weeks', to='stablemanager.Pilot')),
                ('rank', models.ForeignKey(to='warbook.PilotRank')),
            ],
            options={
                'db_table': 'stablemanager_pilotweek',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotWeekTraits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=50, null=True, blank=True)),
                ('pilot_week', models.ForeignKey(to='stablemanager.PilotWeek')),
                ('trait', models.ForeignKey(to='warbook.PilotTrait')),
            ],
            options={
                'db_table': 'stablemanager_pilotweektraits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stable_name', models.CharField(max_length=200)),
                ('reputation', models.IntegerField(default=0)),
                ('house', models.ForeignKey(to='warbook.House', null=True)),
                ('owner', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
                ('stable_disciplines', models.ManyToManyField(to='warbook.PilotTraitGroup')),
                ('supply_contract', models.ManyToManyField(to='warbook.Technology')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StableMech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mech_name', models.CharField(max_length=20, null=True, blank=True)),
                ('purchased_as', models.ForeignKey(to='warbook.MechDesign')),
                ('signature_of', models.ForeignKey(blank=True, to='stablemanager.Pilot', null=True)),
                ('stable', models.ForeignKey(blank=True, to='stablemanager.Stable', null=True)),
            ],
            options={
                'db_table': 'stablemanager_mech',
                'verbose_name': 'Mech',
                'verbose_name_plural': 'Mechs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StableMechWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_design', models.ForeignKey(to='warbook.MechDesign')),
                ('signature_of', models.ForeignKey(blank=True, to='stablemanager.Pilot', null=True)),
                ('stablemech', models.ForeignKey(to='stablemanager.StableMech')),
            ],
            options={
                'db_table': 'stablemanager_mechweek',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StableWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opening_balance', models.IntegerField()),
                ('next_week', models.ForeignKey(related_name='prev_week', to='stablemanager.StableWeek', null=True)),
                ('stable', models.ForeignKey(related_name='ledger', to='stablemanager.Stable')),
                ('week', models.ForeignKey(to='campaign.BroadcastWeek')),
            ],
            options={
                'db_table': 'stablemanager_stableweek',
                'verbose_name': 'StableWeek',
                'verbose_name_plural': 'Ledgers',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stableweek',
            unique_together=set([('stable', 'week')]),
        ),
        migrations.AddField(
            model_name='stablemechweek',
            name='stableweek',
            field=models.ForeignKey(blank=True, to='stablemanager.StableWeek', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='traits',
            field=models.ManyToManyField(to='warbook.PilotTrait', through='stablemanager.PilotWeekTraits', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='week',
            field=models.ForeignKey(to='stablemanager.StableWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilottrainingevent',
            name='pilot_week',
            field=models.ForeignKey(related_name='training', to='stablemanager.PilotWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilottrainingevent',
            name='training',
            field=models.ForeignKey(to='warbook.TrainingCost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilot',
            name='stable',
            field=models.ForeignKey(related_name='pilots', blank=True, to='stablemanager.Stable'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pilot',
            unique_together=set([('stable', 'pilot_callsign')]),
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ledger',
            field=models.ForeignKey(related_name='entries', to='stablemanager.StableWeek'),
            preserve_default=True,
        ),
    ]
