# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0020_pilotweek_removed'),
    ]

    operations = [
        migrations.AddField(
            model_name='stableweek',
            name='ledger_interest',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stablemanager.LedgerItem'),
            preserve_default=True,
        ),
    ]
