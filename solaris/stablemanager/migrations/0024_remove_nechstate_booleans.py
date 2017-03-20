# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0023_stablemechweek_mech_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stablemechweek',
            name='cored',
        ),
        migrations.RemoveField(
            model_name='stablemechweek',
            name='removed',
        ),
    ]
