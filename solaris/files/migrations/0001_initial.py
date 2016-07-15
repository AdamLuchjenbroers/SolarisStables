# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import solaris.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0015_refresh_mechlists'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempMechFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssw_file', models.FileField(upload_to=solaris.files.models.uuid_tempfile)),
                ('mech_name', models.CharField(max_length=50, null=True, blank=True)),
                ('mech_code', models.CharField(max_length=50, null=True, blank=True)),
                ('is_omni', models.BooleanField(default=False)),
                ('bv', models.IntegerField(null=True, blank=True)),
                ('cost', models.IntegerField(null=True, blank=True)),
                ('tons', models.IntegerField(null=True, blank=True)),
                ('motive_type', models.CharField(max_length=20, null=True, blank=True)),
                ('techbase', models.CharField(max_length=20, null=True, blank=True)),
                ('design', models.ForeignKey(blank=True, to='warbook.MechDesign', null=True)),
            ],
            options={
                'db_table': 'temp_mechfile',
                'verbose_name': 'Temp Mech',
                'verbose_name_plural': 'Temp Mechs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TempMechLoadout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('omni_loadout', models.CharField(max_length=30, null=True, blank=True)),
                ('bv', models.IntegerField(null=True, blank=True)),
                ('cost', models.IntegerField(null=True, blank=True)),
                ('design', models.ForeignKey(blank=True, to='warbook.MechDesign', null=True)),
                ('loadout_for', models.ForeignKey(related_name='loadouts', to='files.TempMechFile')),
            ],
            options={
                'db_table': 'temp_mechconfig',
                'verbose_name': 'Temp Mech Config',
                'verbose_name_plural': 'Temp Mech Configs',
            },
            bases=(models.Model,),
        ),
    ]
