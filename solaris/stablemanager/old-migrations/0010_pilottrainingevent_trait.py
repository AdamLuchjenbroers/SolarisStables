# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0010_add_trait_trainingcost'),
        ('stablemanager', '0009_add_fame'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilottrainingevent',
            name='trait',
            field=models.ForeignKey(blank=True, to='warbook.PilotTrait', null=True),
            preserve_default=True,
        ),
    ]
