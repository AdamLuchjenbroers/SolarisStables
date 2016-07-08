'''
Created on 15 Nov 2015

Takes a list of mech names available to the specified house or group
(one per line) and attempts to match them to mechs loaded in the current 
database before adding them to that houses production mech list.
'''


from solaris.warbook.mech.models import MechDesign
from solaris.warbook.models import House


def createMatchingDict(MechDesign=MechDesign):
    designs = MechDesign.objects.all()
    matching = {}
    
    for mech in designs:        
        if  mech.omni_loadout == 'Base' or mech.omni_loadout == None:
            matching['%s %s' % (mech.mech_name, mech.mech_code)] = mech
            matching[mech.mech_code] = mech
        
            #To catch a few cases where the name is inconsistently capitalized
            matching['%s %s' % (mech.mech_name.title(), mech.mech_code)] = mech
        else:
            matching['%s %s%s' % (mech.mech_name, mech.mech_code, mech.omni_loadout)] = mech
            matching['%s %s %s' % (mech.mech_name, mech.mech_code, mech.omni_loadout)] = mech
        
    return matching

def matchFromListFile(house_name, house_list, match_dict=None, live=False, House=House):
    if match_dict == None:
        match_dict = createMatchingDict()
    
    mech_list = open(house_list)
    house = House.objects.get(house=house_name)
    
    for line in mech_list:
        match_name = line.rstrip()
        
        if match_name in match_dict:
            if live:
                match_mech = match_dict[match_name]
                house.produced_designs.add(match_mech)
        elif not live:
            print "Failed to match %s" % match_name

