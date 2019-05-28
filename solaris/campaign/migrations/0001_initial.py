# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('urlname', models.CharField(unique=True, max_length=30)),
                ('campaign_state', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Preparation'), (b'A', b'Active'), (b'C', b'Complete')])),
                ('invite_only', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'campaign',
                'verbose_name': 'Campaign',
            },
            bases=(models.Model,),
        ),
    ]
