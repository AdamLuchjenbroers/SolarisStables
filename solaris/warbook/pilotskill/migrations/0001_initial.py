# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PilotAbility',
            fields=[
            ],
            options={
                'verbose_name': 'Pilot Ability',
                'proxy': True,
                'verbose_name_plural': 'Pilot Abilities',
            },
            bases=('warbook.pilottrait',),
        ),
    ]
