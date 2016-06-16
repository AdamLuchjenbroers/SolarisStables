# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0015_pilotweek_rank_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='reputation_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
