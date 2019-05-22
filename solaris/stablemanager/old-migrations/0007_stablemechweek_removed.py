# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0006_resize_ledger_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='stablemechweek',
            name='removed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
