# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0018_actiongroup_actiontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actiontype',
            name='group',
            field=models.ForeignKey(related_name='actions', to='warbook.ActionGroup'),
            preserve_default=True,
        ),
    ]
