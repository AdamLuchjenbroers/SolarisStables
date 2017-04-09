# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_startingpilottemplate_fame'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcastweek',
            name='week_started',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='actions_per_week',
            field=models.IntegerField(default=20, verbose_name=20),
            preserve_default=False,
        ),
    ]
