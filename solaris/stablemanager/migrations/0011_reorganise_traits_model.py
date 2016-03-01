# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0010_pilottrainingevent_trait'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pilotweek',
            name='traits',
        ),
        migrations.AlterField(
            model_name='pilotweektraits',
            name='pilot_week',
            field=models.ForeignKey(related_name='traits', to='stablemanager.PilotWeek'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pilotweektraits',
            unique_together=set([('pilot_week', 'trait')]),
        ),
    ]
