from math import ceil

critical_funcs = (
	('fixed'   , 'Fixed Criticals'),
	('masc'    , 'MASC'),
	('melee'  ,'Melee Weapon'),
	('targetting_computer', 'Targetting Computer'),
)

def fixed(self, mech=None):
    return self.critical_factor
    
def masc(self, mech=None):
    return ceil( mech.tonnage * 0.05 )

def melee(self, mech=None):
    return ceil( mech.tonnage / self.critical_factor )   
   
def targetting_computer(self, mech):
    return ceil(mech.directfire_tonnage() / 4.0)