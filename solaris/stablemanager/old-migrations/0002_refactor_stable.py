# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0001_initial'),
        ('campaign', '0002_add_campaign_model'),
        ('stablemanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stableweek',
            options={'verbose_name': 'Stable Week', 'verbose_name_plural': 'Stable Weeks'},
        ),
        migrations.RemoveField(
            model_name='stable',
            name='reputation',
        ),
        migrations.RemoveField(
            model_name='stable',
            name='supply_contract',
        ),
        migrations.RemoveField(
            model_name='stablemech',
            name='mech_name',
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_mechdesign',
            field=models.ForeignKey(blank=True, to='warbook.MechDesign', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_pilot',
            field=models.ForeignKey(blank=True, to='stablemanager.Pilot', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_pilot_week',
            field=models.ForeignKey(blank=True, to='stablemanager.PilotWeek', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_stablemech',
            field=models.ForeignKey(blank=True, to='stablemanager.StableMech', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_stablemech_week',
            field=models.ForeignKey(blank=True, to='stablemanager.StableMechWeek', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stable',
            name='campaign',
            field=models.ForeignKey(to='campaign.Campaign', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stableweek',
            name='reputation',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stableweek',
            name='supply_contracts',
            field=models.ManyToManyField(to='warbook.Technology'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stableweek',
            name='supply_mechs',
            field=models.ManyToManyField(to='warbook.MechDesign'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilotweek',
            name='week',
            field=models.ForeignKey(related_name='pilots', to='stablemanager.StableWeek'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stablemechweek',
            name='stableweek',
            field=models.ForeignKey(related_name='mechs', blank=True, to='stablemanager.StableWeek', null=True),
            preserve_default=True,
        ),
    ]
