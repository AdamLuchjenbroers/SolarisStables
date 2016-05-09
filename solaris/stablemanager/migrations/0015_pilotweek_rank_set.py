# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0014_new_pilot_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotweek',
            name='rank_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
