# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0007_add_received_tp'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='house_group',
            field=models.CharField(default=b'I', max_length=1, choices=[(b'I', b'Inner Sphere'), (b'M', b'Mercenaries'), (b'P', b'Periphery'), (b'C', b'Clan')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='house',
            name='selectable_disciplines',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='house',
            name='stable_valid',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
