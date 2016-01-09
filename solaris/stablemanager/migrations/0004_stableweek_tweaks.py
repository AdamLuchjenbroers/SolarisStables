# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0003_add_repairbill_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='stablemechweek',
            name='cored',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stablemechweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, blank=True, to='stablemanager.StableMechWeek'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stableweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, to='stablemanager.StableWeek'),
            preserve_default=True,
        ),
    ]
