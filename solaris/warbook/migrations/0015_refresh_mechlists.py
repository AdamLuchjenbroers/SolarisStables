# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

from solaris.utilities.data.housemechs import matchFromListFile, createMatchingDict

productionLists = [
    ('House Liao'   , 'mechs.liao.txt'   ),
    ('House Kurita' , 'mechs.kurita.txt' ),
    ('House Davion' , 'mechs.davion.txt' ),
    ('House Steiner', 'mechs.steiner.txt'),
    ('House Marik'  , 'mechs.marik.txt'  ),
    ('ComStar'      , 'mechs.comstar.txt'),
]
    
def load_productionlists(apps, schema_editor):
    mech_class = apps.get_model('warbook', 'MechDesign')
    match_dict = createMatchingDict(MechDesign=mech_class)
    house_class = apps.get_model('warbook', 'House')
    
    for (house, filename) in productionLists:
        print "Loading mech list for %s [%s]" % (house, filename)
        full_path = '%s/data/excluded/%s' % (settings.BASE_DIR, filename)
        matchFromListFile(house, full_path, match_dict=match_dict, live=True, House=house_class)  

def rebuild_required_techs(apps, schema_editor):    
    MechDesign = apps.get_model('warbook','MechDesign')
    Equipment = apps.get_model('warbook','Equipment')
    Technology = apps.get_model('warbook','Technology')
    
    for mech in MechDesign.objects.all():
        mech.required_techs.clear()
        
        for item in Equipment.objects.filter(id__in=mech.loadout.all().values('equipment')):
            mech.required_techs.add(*item.supplied_by.all())
        
        if mech.is_omni:
            mech.required_techs.add(Technology.objects.get(name='Omnimechs'))

def derive_mech_tiers(apps, schema_editor):
    MechDesign = apps.get_model('warbook','MechDesign')
    for mech in MechDesign.objects.all():
       mech.tier = mech.required_techs.aggregate(models.Max('tier'))['tier__max']
       mech.save() 

    
def noop(apps, schema_editor):
    # Why bother to delete from tables that are being dropped in the
    # same operation.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0014_convert_blurb'),
    ]

    operations = [
        migrations.RunPython(load_productionlists, reverse_code=noop),
        migrations.RunPython(rebuild_required_techs, reverse_code=noop),
        migrations.RunPython(derive_mech_tiers, reverse_code=noop),
    ]
