# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0003_add_repairbill_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilotweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stablemanager.PilotWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stablemechweek',
            name='cored',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stablemechweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stablemanager.StableMechWeek'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stableweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, to='stablemanager.StableWeek'),
            preserve_default=True,
        ),
    ]
