# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate_delivery_set(apps, schema_editor):
    StableMechWeek = apps.get_model('stablemanager', 'StableMechWeek')

    for smw in StableMechWeek.objects.exclude(next_week=None):
        if smw.next_week.delivery != smw.delivery - 1:
            smw.delivery_set = True
            smw.save()

class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0024_remove_mechstate_booleans'),
    ]

    operations = [
        migrations.AddField(
            model_name='stablemechweek',
            name='delivery_set',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stablemechweek',
            name='mech_status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'O', b'Fully Operational'), (b'X', b'Cored'), (b'D', b'On Display (Honours)'), (b'R', b'To Be Removed'), (b'A', b'Marked For Auction'), (b'-', b'Removed (Hidden)')]),
            preserve_default=True,
        ),
        migrations.RunPython(populate_delivery_set),
    ]
