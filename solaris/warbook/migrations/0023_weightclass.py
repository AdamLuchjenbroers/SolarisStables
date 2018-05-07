# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0022_fightinfo_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('lower', models.IntegerField()),
                ('upper', models.IntegerField()),
                ('in_use', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['lower'],
                'db_table': 'warbook_weightclass',
                'verbose_name': 'Weight Class',
                'verbose_name_plural': 'Weight Classes',
            },
            bases=(models.Model,),
        ),
    ]
