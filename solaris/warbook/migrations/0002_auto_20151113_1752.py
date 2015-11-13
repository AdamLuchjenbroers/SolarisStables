# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='fcs_apollo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipment',
            name='fcs_artemis_iv',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipment',
            name='fcs_artemis_v',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='house',
            name='produced_designs',
            field=models.ManyToManyField(to='warbook.MechDesign', db_table=b'warbook_house_x_mechdesign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='technology',
            name='access_to',
            field=models.ManyToManyField(to='warbook.Equipment', db_table=b'warbook_tech_x_equipment'),
            preserve_default=True,
        ),
    ]
