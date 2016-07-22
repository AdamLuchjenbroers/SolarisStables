# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

import solaris.stablemanager.models

def derive_stable_slugs(apps, schema_editor):
    Stable = apps.get_model('stablemanager', 'Stable')
    
    for stable in Stable.objects.all():
        stable.stable_slug = slugify(stable.stable_name) 
        stable.save()

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0018_pilotweek_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='stable',
            name='stable_bg',
            field=models.ImageField(null=True, upload_to=solaris.stablemanager.models.stable_bg_path, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stable',
            name='stable_icon',
            field=models.ImageField(null=True, upload_to=solaris.stablemanager.models.stable_icon_path, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stable',
            name='stable_slug',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(derive_stable_slugs, reverse_code=noop),
    ]
