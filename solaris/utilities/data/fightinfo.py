from solaris.warbook.fightinfo.models import WeightClass, FightGroup, FightType

from .csvtools import csv_import_to_model

weightclass_fields = ['name', 'lower', 'upper']
fightgroup_fields=['name', 'order']
fighttype_fields = ['group', 'name', 'order', 'urlname', 'blurb', 'rules', 'is_simulation']

def map_fightgroup(value):
    return FightGroup.objects.get(name=value).id

def load_weightclass_csv(csvfile, csvfields=weightclass_fields, WeightClass=WeightClass):
    csv_import_to_model(csvfile, WeightClass, csvfields, keyFields=('name',), booleanFields=())

def load_fightgroup_csv(csvfile, csvfields=fightgroup_fields, FightGroup=FightGroup):
    csv_import_to_model(csvfile, FightGroup, csvfields, keyFields=('name',), booleanFields=())

def load_fighttype_csv(csvfile, csvfields=fighttype_fields, FightType=FightType):
    csv_import_to_model(csvfile, FightType, csvfields, keyFields=('group','name',), booleanFields=('is_simulation',), mapFunctions={'group' : map_fightgroup})

