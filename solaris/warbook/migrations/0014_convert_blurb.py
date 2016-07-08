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
        migrations.RunPython(render_fields, reverse_code=render_fields),
    ]
