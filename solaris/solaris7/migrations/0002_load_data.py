# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command

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
        ('solaris7', '0001_initial'),
        ('campaign', '0001_initial'),
        ('warbook', '0002_load_data'),
    ]

    operations = [
        migrations.RunPython(setup_campaign, reverse_code=noop),
        migrations.RunPython(load_zodiac, reverse_code=noop),
        migrations.RunPython(create_initial_week, reverse_code=noop),
        migrations.RunPython(populate_templates, reverse_code=noop),
    ]
