# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0006_track_week_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='actions_per_week',
        ),
        migrations.AddField(
            model_name='campaign',
            name='actions_duringweek',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='actions_startweek',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
