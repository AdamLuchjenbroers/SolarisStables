# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0007_stablemechweek_removed'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='training_points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
