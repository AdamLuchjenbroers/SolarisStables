from math import ceil

critical_funcs = (
	('Fixed Criticals', 'fixed'),
	('MASC', 'masc')
)

def fixed(self, mech):
    return self.critical_factor
    
def masc(self, mech):
    return ceil( mech.tonnage * 0.05 )

def melee(self, mech):
    return ceil( mech.tonnage / self.critical_factor )