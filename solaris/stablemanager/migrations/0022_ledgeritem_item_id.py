# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0021_stableweek_ledger_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledgeritem',
            name='item_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
