# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0019_actiontype_groupfix'),
        ('stablemanager', '0025_add_delivery_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='StableAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.IntegerField()),
                ('notes', models.CharField(max_length=256, null=True, blank=True)),
                ('action', models.ForeignKey(to='warbook.ActionType')),
                ('week', models.ForeignKey(related_name='actions', to='stablemanager.StableWeek')),
            ],
            options={
                'db_table': 'stablemanager_actions',
                'verbose_name': 'Stable Action',
                'verbose_name_plural': 'Stable Actions',
            },
            bases=(models.Model,),
        ),
    ]
