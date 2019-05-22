# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

def fix_missing_campaign(apps, schema_editor):
    Campaign = apps.get_model('campaign','Campaign')
    BroadcastWeek = apps.get_model('campaign','BroadcastWeek')

    default = Campaign.objects.get(name=settings.CURRENT_CAMPAIGN)
    for week in BroadcastWeek.objects.filter(campaign=None):
        week.campaign = default
        week.save()

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_startingpilottemplate'),
    ]

    operations = [
        migrations.RunPython(fix_missing_campaign, reverse_code=noop),
        migrations.AlterField(
            model_name='broadcastweek',
            name='campaign',
            field=models.ForeignKey(related_name='weeks', to='campaign.Campaign'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='broadcastweek',
            name='next_week',
            field=models.OneToOneField(related_name='prev_week', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='campaign.BroadcastWeek'),
            preserve_default=True,
        ),
    ]
