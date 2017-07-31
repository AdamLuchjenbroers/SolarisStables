# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

weight_data = (
 ('Ultralight', 20, 25),
 ('Skirmisher', 20, 40),
 ('Striker', 45, 60),
 ('Battler', 65, 80),
 ('Assault', 85, 100),
)

def setup_weightclasses(apps, schema_editor):
    WeightClass = apps.get_model('warbook', 'WeightClass')

    for (name, lower, upper) in weight_data:
        WeightClass.objects.create(name=name, lower=lower, upper=upper)
    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0020_fightinfo_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('lower', models.IntegerField()),
                ('upper', models.IntegerField()),
                ('in_use', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['lower'],
                'db_table': 'warbook_weightclass',
                'verbose_name': 'Weight Class',
                'verbose_name_plural': 'Weight Classes',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(setup_weightclasses, reverse_code=noop),
    ]
