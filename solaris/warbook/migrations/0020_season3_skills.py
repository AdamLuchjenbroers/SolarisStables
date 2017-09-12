# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0019_actiontype_groupfix'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilottraitgroup',
            name='rank_restricted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilottraitgroup',
            name='discipline_type',
            field=models.CharField(default=b'I', max_length=1, choices=[(b'T', b'Training'), (b'S', b'Secondary Skills'), (b'I', b'Issues'), (b'O', b'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trainingcost',
            name='training',
            field=models.CharField(max_length=1, choices=[(b'P', b'Piloting'), (b'G', b'Gunnery'), (b'S', b'Skills'), (b'2', b'Secondary Skills'), (b'T', b'Other Traits')]),
            preserve_default=True,
        ),
    ]
