# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0008_house_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='house_disciplines',
            field=models.ManyToManyField(to='warbook.PilotTraitGroup', db_table=b'warbook_house_x_discipline', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='house',
            name='produced_designs',
            field=models.ManyToManyField(to='warbook.MechDesign', db_table=b'warbook_house_x_mechdesign', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='house',
            name='house',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
    ]
