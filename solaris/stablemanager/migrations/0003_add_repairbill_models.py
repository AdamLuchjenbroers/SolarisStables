# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0004_add_tech_tiers'),
        ('stablemanager', '0002_refactor_stable'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete', models.BooleanField(default=False)),
                ('mech', models.ForeignKey(to='warbook.MechDesign')),
                ('stableweek', models.ForeignKey(related_name='repairs', to='stablemanager.StableMechWeek')),
            ],
            options={
                'db_table': 'stablemanager_repairbill',
                'verbose_name': 'Repair Bill',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepairBillCrit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.IntegerField()),
                ('critted', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'stablemanager_repair_line_x_loc',
                'verbose_name': 'Repair Bill Crit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepairBillLineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('line_type', models.CharField(max_length=1, choices=[(b'A', b'Armour'), (b'S', b'Structure'), (b'Q', b'Equipment'), (b'M', b'Ammunition'), (b'L', b'Labour Cost')])),
                ('bill', models.ForeignKey(related_name='lineitems', to='stablemanager.RepairBill')),
                ('item', models.ForeignKey(blank=True, to='warbook.MechEquipment', null=True)),
            ],
            options={
                'db_table': 'stablemanager_repairbill_line',
                'verbose_name': 'Repair Bill Line',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepairBillLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('armour_lost', models.IntegerField()),
                ('structure_lost', models.IntegerField()),
                ('bill', models.ForeignKey(related_name='locations', to='stablemanager.RepairBill')),
                ('location', models.ForeignKey(to='warbook.MechDesignLocation')),
            ],
            options={
                'db_table': 'stablemanager_repairbill_loc',
                'verbose_name': 'Repair Bill Location',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='repairbillcrit',
            name='lineitem',
            field=models.ForeignKey(to='stablemanager.RepairBillLineItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repairbillcrit',
            name='location',
            field=models.ForeignKey(to='stablemanager.RepairBillLocation'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='stablemech',
            name='signature_of',
        ),
        migrations.AddField(
            model_name='ledgeritem',
            name='ref_repairbill',
            field=models.OneToOneField(related_name='ledger', null=True, blank=True, to='stablemanager.RepairBill'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stablemechweek',
            name='signature_of',
            field=models.ForeignKey(related_name='signature_mechs', blank=True, to='stablemanager.Pilot', null=True),
            preserve_default=True,
        ),
    ]
