# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0019_add_stable_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotweek',
            name='removed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
