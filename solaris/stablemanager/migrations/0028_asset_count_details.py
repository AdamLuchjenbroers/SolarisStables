# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0027_track_week_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='mechs_count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stableweek',
            name='pilot_count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stableweek',
            name='asset_count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
