# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0013_pilot_trait_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotweek',
            name='blackmarks_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stablemechweek',
            name='delivery',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilotdeferment',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
