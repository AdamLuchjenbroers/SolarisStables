from math import ceil

critical_funcs = (
	('fixed'   , 'Fixed Criticals'),
	('masc'    , 'MASC'),
	('melee'  ,'Melee Weapon'),
	('targetting_computer', 'Targetting Computer'),
        ('retractable', 'Retractable Blade'),
        ('by_class', 'By Weight Class'),
        ('per_leg', 'Per Leg'),
)

def fixed(self, mech=None):
    return int(self.critical_factor)
    
def masc(self, mech=None):
    return int(mech.tonnage * 0.05 )

def melee(self, mech=None):
    return int(ceil( mech.tonnage / self.critical_factor ))   
   
def targetting_computer(self, mech=None):
    if mech:
        return int(ceil(float(mech.directfire_tonnage()) / 4.0))
    else:
        return None

def retractable(self, mech=None):
    return int(ceil( mech.tonnage / self.critical_factor )) + 1 

def by_class(self, mech=None):
    if mech.tonnage < 40:
        return self.critical_factor
    elif mech.tonnage < 60:
        return self.critical_factor * 2
    elif mech.tonnage < 80:
        return self.critical_factor * 3
    else:
        return self.critical_factor * 4

def per_leg(self, mech=None):
    if mech.motive_type == 'Q':
        return 4 * self.critical_factor
    else:
        return 2 * self.critical_factor
