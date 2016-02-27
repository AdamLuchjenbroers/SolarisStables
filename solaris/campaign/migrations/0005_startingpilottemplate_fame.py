# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_template_fame(apps, schema_editor):
    StartingPilotTemplate = apps.get_model('campaign','StartingPilotTemplate')

    template_fame = {'Star': '1', 'Champion': '3'}
    for template in StartingPilotTemplate.objects.filter(rank__rank__in=template_fame.keys()):
        template.fame = template_fame[template.rank.rank]
        template.save()
    
def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_link_week_to_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='startingpilottemplate',
            name='fame',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RunPython(add_template_fame, reverse_code=noop),
    ]
