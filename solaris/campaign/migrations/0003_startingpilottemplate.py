# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate_templates(apps, schema_editor):
    StartingPilotTemplate = apps.get_model('campaign','StartingPilotTemplate')
    Campaign = apps.get_model('campaign','StartingPilotTemplate')
    PilotRank = apps.get_model('warbook', 'PilotRank')

    templates = [
       ('Champion' , 1, 3, 4),
       ('Star'     , 4, 4, 5),
       ('Contender', 5, 5, 6),
       ('Rookie'   , 4, 5, 6),
    ]

    for c in Campaign.objects.all():
        for (rank, count, gunnery, pilotting) in templates:
            StartingPilotTemplate.objects.create(
                campaign = c
            ,   rank = PilotRank.objects.get(rank=rank)
            ,   count = count
            ,   gunnery = gunnery
            ,   pilotting = pilotting
            )
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_add_campaign_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartingPilotTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('piloting', models.IntegerField()),
                ('gunnery', models.IntegerField()),
                ('campaign', models.ForeignKey(related_name='initial_pilots', to='campaign.Campaign')),
                ('rank', models.ForeignKey(to='warbook.PilotRank')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(populate_templates, reverse_code=noop),
    ]
