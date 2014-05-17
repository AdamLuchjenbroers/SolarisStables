from math import ceil

tonnage_funcs = (
	('fixed'  , 'Fixed Tonnage'),
	('jumpjet', 'Jumpjet'),
	('masc'   , 'MASC'),
	('melee'  ,'Melee Weapon'),
	('armour' , 'Armour'),
	('engine' , 'Engine'),
	('gyro'   , 'Gyro'),
	('structure', 'Internal Structure')
)

def fixed(self, mech):
    return self.tonnage_factor

def jumpjet(self, mech):
    if mech.tonnage <= 55:
        return 0.5 * self.tonnage_factor
    if mech.tonnage > 55 and mech.tonnage <= 85:
        return 1.0 * self.tonnage_factor
    else:
        #90+ Tons
        return 2.0 * self.tonnage_factor 
    
def masc(self, mech):
    return ceil( mech.tonnage * 0.05 )

def melee(self, mech):
    return ceil( mech.tonnage / self.tonnage_factor )

def armour(self, mech, units=None):
    if units == None:
        units = mech.total_armour()
    
    return ceil(units / (self.tonnage_factor * 8)) / 2

def engine(self, mech):
    #FIXME
    return 0
   
def structure(self, mech):
    return ceil((mech.tonnage * self.tonnage_factor * 2) / 10)/2
    
def gyro(self, mech):
    return ceil(mech.engine_rating / 100.0) * self.tonnage_factor 