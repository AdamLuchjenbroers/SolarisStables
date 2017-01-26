# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0016_add_blacktech_tier'),
        ('stablemanager', '0021_pilottraitevent_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='HonouredDead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('removed', models.BooleanField(default=False)),
                ('display_mech', models.ForeignKey(blank=True, to='warbook.MechDesign', null=True)),
                ('next_week', models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stablemanager.HonouredDead')),
                ('pilot', models.ForeignKey(to='stablemanager.Pilot')),
                ('week', models.ForeignKey(related_name='honoured', to='stablemanager.StableWeek')),
            ],
            options={
                'ordering': ('pilot__pilot_callsign',),
                'db_table': 'stablemanager_honoured_dead',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='honoureddead',
            unique_together=set([('pilot', 'week')]),
        ),
    ]
