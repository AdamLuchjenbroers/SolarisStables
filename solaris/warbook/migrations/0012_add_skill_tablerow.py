# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0011_pilotrank_prominence_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilottrait',
            name='item',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilottrait',
            name='table',
            field=models.IntegerField(default=1, choices=[(1, b'[1-3]'), (2, b'[4-6]')]),
            preserve_default=True,
        ),
    ]
