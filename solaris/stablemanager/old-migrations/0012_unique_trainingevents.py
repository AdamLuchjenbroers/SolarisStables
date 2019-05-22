# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0011_reorganise_traits_model'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pilottrainingevent',
            unique_together=set([('pilot_week', 'training')]),
        ),
    ]
