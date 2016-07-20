# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def prefill_pilotweek_status(apps, schema_editor):
    PilotWeek = apps.get_model('stablemanager', 'PilotWeek')
    
    for pw in PilotWeek.objects.all():
        if pw.fame_set or pw.wounds_set or pw.blackmarks_set:
            pw.status = 'X'
            pw.save()

def noop(apps, schema_editor):
     #Why reset the values of a column we're dropping..
     pass      

class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0017_stablemechweek_config_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotweek',
            name='status',
            field=models.CharField(default=b'-', max_length=1, choices=[(b'X', b'Fielded'), (b'-', b'Available'), (b'R', b'Reserved')]),
            preserve_default=True,
        ),
        migrations.RunPython(prefill_pilotweek_status, reverse_code=noop),
    ]
