from math import ceil

critical_funcs = (
	('fixed'   , 'Fixed Criticals'),
	('masc'    , 'MASC'),
	('melee'  ,'Melee Weapon'),
	('targetting_computer', 'Targetting Computer'),
)

def fixed(self, mech=None):
    return int(self.critical_factor)
    
def masc(self, mech=None):
    return int(ceil( mech.tonnage * 0.05 ))

def melee(self, mech=None):
    return int(ceil( mech.tonnage / self.critical_factor ))   
   
def targetting_computer(self, mech=None):
    if mech:
        return int(ceil(float(mech.directfire_tonnage()) / 4.0))
    else:
        return None