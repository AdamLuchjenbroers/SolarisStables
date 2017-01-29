# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def setup_honours(apps, schema_editor):
    PilotRank = apps.get_model('warbook','PilotRank')
    
    for rank_name in ('Star', 'Champion'):
        rank = PilotRank.objects.get(rank=rank_name)
        rank.receive_honours = True
        rank.save()

def noop(apps, schema_editor):
    # Why bother to delete from columns that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0016_add_blacktech_tier'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotrank',
            name='receive_honours',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RunPython(setup_honours, reverse_code=noop),
    ]
