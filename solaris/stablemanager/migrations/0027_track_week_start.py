# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0026_stableaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='asset_count',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stableweek',
            name='week_started',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
