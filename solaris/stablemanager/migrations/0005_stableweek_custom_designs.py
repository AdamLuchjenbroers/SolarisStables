# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0006_load_mechs'),
        ('stablemanager', '0004_stableweek_tweaks'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='custom_designs',
            field=models.ManyToManyField(related_name='produced_by', to='warbook.MechDesign'),
            preserve_default=True,
        ),
    ]
