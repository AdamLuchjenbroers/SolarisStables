# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def setup_campaign(apps, schema_editor):
    Campaign = apps.get_model('campaign', 'Campaign')
    theCampaign = Campaign.objects.create(name='Solaris7', initial_balance=75000000)
    
    Technology = apps.get_model('warbook', 'Technology')
    # Initial techtree is all Green + White techs
    for tech in Technology.objects.filter(tier__lte=1):
        theCampaign.initial_contracts.add(tech)

    theCampaign.save()
     
    Zodiac = apps.get_model('campaign', 'Zodiac')
    for sign in Zodiac.objects.all():
        sign.campaign = theCampaign
        sign.save()
    
    BroadcastWeek = apps.get_model('campaign', 'BroadcastWeek')
    for week in BroadcastWeek.objects.all():
        week.campaign = theCampaign
        week.save() 
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
        ('warbook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('initial_balance', models.IntegerField()),
                ('initial_contracts', models.ManyToManyField(to='warbook.Technology')),
            ],
            options={
                'db_table': 'campaign',
                'verbose_name': 'Campaign',
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='BroadcastWeekManager',
        ),
        migrations.AddField(
            model_name='broadcastweek',
            name='campaign',
            field=models.ForeignKey(blank=True, to='campaign.Campaign', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='zodiac',
            name='campaign',
            field=models.ForeignKey(blank=True, to='campaign.Campaign', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(setup_campaign, reverse_code=noop),
    ]
