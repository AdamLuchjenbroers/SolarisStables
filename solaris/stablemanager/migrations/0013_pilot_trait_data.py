# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0010_add_trait_trainingcost'),
        ('stablemanager', '0012_unique_trainingevents'),
    ]

    operations = [
        migrations.CreateModel(
            name='PilotDeferment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=50, null=True, blank=True)),
                ('duration', models.IntegerField()),
                ('duration_set', models.BooleanField(default=False)),
                ('deferred', models.ForeignKey(to='warbook.PilotTrait')),
                ('next_week', models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stablemanager.PilotDeferment')),
                ('pilot_week', models.ForeignKey(related_name='deferred', to='stablemanager.PilotWeek')),
            ],
            options={
                'ordering': ('pilot_week__pilot__pilot_callsign', '-duration'),
                'db_table': 'stablemanager_issuedeferred',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PilotTraitEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=50, null=True, blank=True)),
                ('pilot_week', models.ForeignKey(related_name='new_traits', to='stablemanager.PilotWeek')),
                ('trait', models.ForeignKey(to='warbook.PilotTrait')),
            ],
            options={
                'ordering': ('pilot_week__pilot__pilot_callsign', 'trait'),
                'db_table': 'stablemanager_traitevent',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pilottraitevent',
            unique_together=set([('pilot_week', 'trait')]),
        ),
        migrations.AlterUniqueTogether(
            name='pilotdeferment',
            unique_together=set([('pilot_week', 'deferred')]),
        ),
        migrations.AlterModelOptions(
            name='pilottrainingevent',
            options={'ordering': ('training__training', 'training__cost')},
        ),
        migrations.AddField(
            model_name='pilotweek',
            name='blackmarks',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pilottrainingevent',
            unique_together=set([('pilot_week', 'training'), ('pilot_week', 'trait')]),
        ),
    ]
