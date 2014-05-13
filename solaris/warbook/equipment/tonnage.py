from math import ceil

tonnage_funcs = (
	('Fixed Tonnage', 'fixed'),
	('Jumpjet', 'jumpjet'),
	('MASC', 'masc'),
	('Melee Weapon', 'melee'),
	('Armour', 'armour'),
)

def fixed(self, mech):
    return self.tonnage_factor

def jumpjet(self, mech):
    if mech.tonnage <= 55:
        return 0.5f * self.tonnage_factor
    if mech.tonnage > 55 and mech.tonnage <= 85:
        return 1.0f * self.tonnage_factor
    else:
        #90+ Tons
        return 2.0f * self.tonnage_factor 
    
def masc(self, mech):
    return ceil( mech.tonnage * 0.05f )

def melee(self, mech):
    return ceil( mech.tonnage / self.tonnage_factor )

def armour(self, mech, units=None)
    if units == None:
		units = mech.total_armour()
    
	return ceil(units / (self.tonnage_factor * 8)) / 2
	