# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def setup_prominence(apps, schema_editor):
    PilotRank = apps.get_model('warbook','PilotRank')
    
    for (prominence, rank_name) in ((2, 'Champion'), (1, 'Star')):
        rank = PilotRank.objects.get(rank=rank_name)
        rank.prominence_factor = prominence
        rank.save()
    
def noop(apps, schema_editor):
    # Why bother to delete from columns that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0010_add_trait_trainingcost'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotrank',
            name='prominence_factor',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RunPython(setup_prominence, reverse_code=noop),
    ]
