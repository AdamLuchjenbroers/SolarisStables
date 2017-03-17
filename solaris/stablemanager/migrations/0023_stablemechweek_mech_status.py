# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_status(apps, schema_editor):
    StableMechWeek = apps.get_model('stablemanager', 'StableMechWeek')
    HonouredDead = apps.get_model('stablemanager', 'HonouredDead')

    for smw in StableMechWeek.objects.all():
        if smw.cored:
            smw.mech_status = 'X'
        elif HonouredDead.objects.filter(week=smw.stableweek, display_mech=smw.stablemech).exists():
            smw.mech_status = 'D'
        elif smw.removed:
            smw.mech_status = 'R'
        else:
            smw.mech_status = 'O'
        smw.save()

    for smw in StableMechWeek.objects.filter(prev_week__mech_status__in=('X','D','R','A')):
        smw.mech_status = '-'
        smw.save()

def noop(apps, schema_editor):
    # Why bother to delete from fields that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('stablemanager', '0022_add_honoureddead'),
    ]

    operations = [
        migrations.AddField(
            model_name='stablemechweek',
            name='mech_status',
            field=models.CharField(default='O', max_length=1, choices=[(b'O', b'Fully Operational'), (b'X', b'Cored'), (b'D', b'On Display (Honours)'), (b'R', b'To Be Removed'), (b'A', b'Marked For Auction'), (b'-', b'Removed (Hidden)')]),
            preserve_default=False,
        ),
        migrations.RunPython(populate_status, reverse_code=noop),
    ]
