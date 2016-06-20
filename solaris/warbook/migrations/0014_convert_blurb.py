# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields

def render_fields(apps, schema_editor):
    PilotTraitGroup = apps.get_model('warbook', 'PilotTraitGroup')
    for p in PilotTraitGroup.objects.all():
        p.save()

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0013_improve_pilottraits'),
    ]

    operations = [
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
        migrations.RunPython(render_fields),
    ]
