# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0023_weightclass'),
        ('campaign', '0007_season3_actions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RosteredFight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purse', models.IntegerField(null=True, blank=True)),
                ('group_tonnage', models.IntegerField(null=True, blank=True)),
                ('group_units', models.IntegerField(default=1)),
                ('fight_class', models.CharField(max_length=40, blank=True)),
                ('fought', models.BooleanField(default=False)),
                ('chassis', models.ForeignKey(blank=True, to='warbook.MechDesign', null=True)),
            ],
            options={
                'ordering': ['fight_type__order', 'group_units', 'weightclass__lower', 'group_tonnage'],
                'db_table': 'campaign_rosteredfight',
                'verbose_name': 'Rostered Fight',
                'verbose_name_plural': 'Rostered Fights',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RosteredFightCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annotation', models.CharField(max_length=20, blank=True)),
                ('condition', models.ForeignKey(to='warbook.FightCondition')),
                ('fight', models.ForeignKey(to='campaign.RosteredFight')),
            ],
            options={
                'db_table': 'campaign_fight_x_condition',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='conditions',
            field=models.ManyToManyField(to='warbook.FightCondition', through='campaign.RosteredFightCondition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_map',
            field=models.ForeignKey(to='warbook.Map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='fight_type',
            field=models.ForeignKey(to='warbook.FightType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='week',
            field=models.ForeignKey(related_name='fights', to='campaign.BroadcastWeek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rosteredfight',
            name='weightclass',
            field=models.ForeignKey(blank=True, to='warbook.WeightClass', null=True),
            preserve_default=True,
        ),
    ]
