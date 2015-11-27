# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.mechs import loadMechFolder
from solaris.utilities.data.housemechs import matchFromListFile, createMatchingDict

def load_mechs(apps, schema_editor):
    loadMechFolder()
    
def clear_mechs(apps, schema_editor):
    MechDesign = apps.get_model('warbook', 'MechDesign')
    
    for mech in MechDesign.objects.all():
        # Clear equipment / mountings tables first before deleting.
        mech.reset_equipment()
        mech.delete()

productionLists = [
    ('House Liao'   , 'mechs.liao.txt'   ),
    ('House Kurita' , 'mechs.kurita.txt' ),
    ('House Davion' , 'mechs.davion.txt' ),
    ('House Steiner', 'mechs.steiner.txt'),
    ('House Marik'  , 'mechs.marik.txt'  ),
    ('ComStar'      , 'mechs.comstar.txt'),
]
    
def load_productionlists(apps, schema_editor):
    match_dict = createMatchingDict()
    
    for (house, filename) in productionLists:
        print "Loading mech list for %s [%s]" % (house, filename)
        full_path = '%s/data/excluded/%s' % (settings.BASE_DIR, filename)
        matchFromListFile(house, full_path, match_dict=match_dict, live=True)  

def derive_mech_tiers(apps, schema_editor):
    Equipment = apps.get_model('warbook','Equipment')
    MechDesign = apps.get_model('warbook','MechDesign')
    for mech in MechDesign.objects.all():
       mech_eq = Equipment.objects.filter(id__in=mech.loadout.all().values('equipment'))   
       mech.tier = mech_eq.aggregate(models.Max('tier'))['tier__max'] 
       mech.save() 

    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0004_add_tech_tiers'),
    ]

    operations = [
        migrations.RunPython(load_mechs, reverse_code=noop),
        migrations.RunPython(load_productionlists, reverse_code=noop),
        migrations.RunPython(derive_mech_tiers, reverse_code=noop),
    ]
