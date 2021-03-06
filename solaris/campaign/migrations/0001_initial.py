# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

import json

def load_zodiac(apps, schema_editor):
    Zodiac = apps.get_model('campaign','Zodiac')
    signs = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Sheep', 'Monkey', 'Rooster', 'Dog', 'Pig']
    last = None

    signs.reverse()
    for s in signs:
        last = Zodiac.objects.create(sign=s, rules='TBA', next=last)
    
    pig = Zodiac.objects.get(sign='Pig')
    pig.next = Zodiac.objects.get(sign='Rat')
    pig.save()

    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

def create_initial_week(apps, schema_editor):
    BroadcastWeek = apps.get_model('campaign','BroadcastWeek')
    Zodiac = apps.get_model('campaign','Zodiac')
    BroadcastWeek.objects.create(week_number=1, sign=Zodiac.objects.get(sign="Rat"))

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_number', models.IntegerField()),
                ('next_week', models.OneToOneField(related_name='prev_week', null=True, blank=True, to='campaign.BroadcastWeek')),
            ],
            options={
                'db_table': 'campaign_broadcastweek',
                'verbose_name': 'Broadcast Week',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BroadcastWeekManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zodiac',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sign', models.CharField(max_length=20)),
                ('rules', models.TextField()),
                ('next', models.OneToOneField(related_name='prev', null=True, to='campaign.Zodiac')),
            ],
            options={
                'db_table': 'campaign_zodiac',
                'verbose_name': 'Zodiac Sign',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='broadcastweek',
            name='sign',
            field=models.ForeignKey(to='campaign.Zodiac'),
            preserve_default=True,
        ),                  
        migrations.RunPython(load_zodiac, reverse_code=noop),
        migrations.RunPython(create_initial_week, reverse_code=noop),
    ]
