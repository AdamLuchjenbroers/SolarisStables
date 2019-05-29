# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

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
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
        ('warbook', '0024_fightinfo_data'),
    ]

    operations = [
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
                ('condition', models.ForeignKey(to='warbook.FightCondition')),
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
            field=models.ManyToManyField(to='warbook.FightCondition', through='solaris7.RosteredFightCondition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_map',
            field=models.ForeignKey(to='warbook.Map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_type',
            field=models.ForeignKey(to='warbook.FightType'),
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
            field=models.ForeignKey(blank=True, to='warbook.WeightClass', null=True),
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
        migrations.RunPython(setup_campaign, reverse_code=noop),
        migrations.RunPython(load_zodiac, reverse_code=noop),
        migrations.RunPython(create_initial_week, reverse_code=noop),
        migrations.RunPython(populate_templates, reverse_code=noop),
    ]
