# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0020_pilotweek_removed'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilottraitevent',
            name='added',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
