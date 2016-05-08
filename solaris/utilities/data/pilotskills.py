from solaris.warbook.pilotskill.models import PilotTrait, PilotTraitGroup
from .csvtools import csv_import_to_model

from decimal import Decimal

trait_fields = ['discipline', 'table', 'item', 'bv_mod', 'name', 'description']

def map_discipline(value):
    return PilotTraitGroup.objects.get(name=value).id

def map_bv(value):
    # A little bit of voodoo, but Decimal choices are unusually finicky.
    return Decimal('%0.3f' % Decimal(value))

def load_pilottrait_csv(csvfile, csvfields=trait_fields, PilotTrait=PilotTrait):
    csv_import_to_model( csvfile, PilotTrait, csvfields, keyFields=('discipline', 'name')
                       , booleanFields=(), mapFunctions={'discipline' : map_discipline, 'bv_mod' : map_bv} )

