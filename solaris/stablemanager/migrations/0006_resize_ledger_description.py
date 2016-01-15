# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0005_stableweek_custom_designs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledgeritem',
            name='description',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
