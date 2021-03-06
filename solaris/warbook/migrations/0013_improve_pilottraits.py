# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solaris.utilities.data.pilotskills import load_pilottrait_csv

from django.db import models, migrations
from django.conf import settings
import markitup.fields

def clear_model(apps, appName, model):
    model = apps.get_model(appName, model)
    model.objects.all().delete()
    
def create_issues_group(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')
    
    PilotTraitGroup.objects.create(name='Pilot Problems', blurb='...', urlname='pilot-issues', discipline_type='I')

def delete_issues_group(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')
    
    PilotTraitGroup.objects.get(urlname='pilot-issues').delete()

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0012_add_skill_tablerow'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilottrait',
            name='_description_rendered',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilottrait',
            name='description',
            field=markitup.fields.MarkupField(no_rendered_field=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilottrait',
            name='table',
            field=models.CharField(default=b'-', max_length=6, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pilottraitgroup',
            name='_blurb_rendered',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilottraitgroup',
            name='blurb',
            field=markitup.fields.MarkupField(no_rendered_field=True),
            preserve_default=True,
        ),
        migrations.RunPython(create_issues_group, reverse_code=delete_issues_group),
    ]
