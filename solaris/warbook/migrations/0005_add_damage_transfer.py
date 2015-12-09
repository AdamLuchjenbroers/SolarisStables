# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def make_transfer_map(apps, schema_editor):
    MechLocation = apps.get_model('warbook', 'MechLocation')

    location = {}
    for loc in MechLocation.objects.all():
        location[loc.location] = loc

    locationMap  = [(limb, 'RT') for limb in ('RA','RL','RRL','RFL')]
    locationMap += [(limb, 'LT') for limb in ('LA','LL','LRL','LFL')]
    locationMap += [(side, 'CT') for side in ('RT','LT')]
    locationMap += [(side, 'RCT') for side in ('RRT','RLT')]

    for (source, transfer) in locationMap:
        location[source].next_damage = location[transfer]
        location[source].save()    

def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0004_add_tech_tiers'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechlocation',
            name='next_damage',
            field=models.ForeignKey(related_name='prev_damage', to='warbook.MechLocation', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mechlocation',
            name='rear_of',
            field=models.ForeignKey(related_name='front_of', to='warbook.MechLocation', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(make_transfer_map, reverse_code=noop),
    ]
