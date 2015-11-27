# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def derive_equipment_tiers(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    for eq in Equipment.objects.all():
        eq.tier = eq.supplied_by.all().aggregate(models.Min('tier'))['tier__min']
        if eq.tier == None:
            eq.tier = 3
        eq.save()

def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0003_load-reference-data'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='tier',
            field=models.IntegerField(default=0, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mechdesign',
            name='tier',
            field=models.IntegerField(default=0, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='technology',
            name='access_to',
            field=models.ManyToManyField(related_name='supplied_by', db_table=b'warbook_tech_x_equipment', to='warbook.Equipment'),
            preserve_default=True,
        ),
        migrations.RunPython(derive_equipment_tiers, reverse_code=noop),
    ]
