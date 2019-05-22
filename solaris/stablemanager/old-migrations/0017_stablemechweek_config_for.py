# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0016_stableweek_reputation_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='stablemechweek',
            name='config_for',
            field=models.ForeignKey(related_name='loadouts', blank=True, to='stablemanager.StableMechWeek', null=True),
            preserve_default=True,
        ),
    ]
