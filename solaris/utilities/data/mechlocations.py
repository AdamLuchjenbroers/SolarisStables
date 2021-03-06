'''
Once-off utility code that populates the Mech Locations table
'''
import os

from solaris.warbook.mech.refdata import locations_all, criticals
from solaris.warbook.mech.models import MechLocation

def generateMechLocations():
    loc = {}
    
    for pair in locations_all:
        code = pair[0]
        (loc[code], created) = MechLocation.objects.get_or_create(location=code, defaults = {'criticals' : criticals(code)})        
        
    # Set up Rear Locations
    loc['RRT'].rear_of = loc['RT']
    loc['RRT'].save()
    loc['RLT'].rear_of = loc['LT']
    loc['RLT'].save()
    loc['RCT'].rear_of = loc['CT']
    loc['RCT'].save()

