# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def setup_trainables(apps, schema_editor):
    PilotRank = apps.get_model('warbook','PilotRank')
    
    for rank_name in ('Rookie', 'Contender'):
        rank = PilotRank.objects.get(rank=rank_name)
        rank.receive_tp = True
        rank.save()
    
def noop(apps, schema_editor):
    # Why bother to delete from columns that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0006_load_mechs'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotrank',
            name='receive_tp',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='cost_func',
            field=models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Cost'), (b'per_ton', b'Per Ton'), (b'structure', b'Structure'), (b'engine', b'Engine'), (b'gyro', b'Gyro'), (b'mech', b'Mech Tonnage'), (b'jumpjet', b'Jumpjet'), (b'per_er', b'By Engine Rating'), (b'masc', b'MASC'), (b'retract', b'Retractable Blade'), (b'drone', b'Drone OS')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='critical_func',
            field=models.CharField(max_length=40, null=True, choices=[(b'fixed', b'Fixed Criticals'), (b'masc', b'MASC'), (b'melee', b'Melee Weapon'), (b'targetting_computer', b'Targetting Computer'), (b'retractable', b'Retractable Blade'), (b'by_class', b'By Weight Class'), (b'per_leg', b'Per Leg')]),
            preserve_default=True,
        ),
        migrations.RunPython(setup_trainables, reverse_code=noop),
    ]
