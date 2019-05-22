# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0008_stableweek_training_points'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pilotweek',
            options={'ordering': ['rank__id', 'skill_gunnery', 'skill_piloting', 'pilot__pilot_callsign']},
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='fame',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='fame_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='wounds_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
