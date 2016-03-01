# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_trait_training(apps, schema_editor):
    TrainingCost = apps.get_model('warbook', 'TrainingCost')
    TrainingCost.objects.create(training='T', train_from=0, train_to=0, cost=0) 

def remove_trait_training(apps, schema_editor):
    TrainingCost = apps.get_model('warbook', 'TrainingCost')
    TrainingCost.objects.filter(training='T').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0009_make_house_fields_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='stable_valid',
            field=models.BooleanField(default=True, verbose_name=b'Available for Stables'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trainingcost',
            name='training',
            field=models.CharField(max_length=1, choices=[(b'P', b'Piloting'), (b'G', b'Gunnery'), (b'S', b'Skills'), (b'T', b'Other Traits')]),
            preserve_default=True,
        ),
        migrations.RunPython(add_trait_training, reverse_code=remove_trait_training),
    ]
