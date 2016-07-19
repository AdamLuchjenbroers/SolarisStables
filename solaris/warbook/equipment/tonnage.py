from math import ceil
from decimal import Decimal

def half_ton(value):
    return Decimal( ceil(value * 2) / 2.0 )

tonnage_funcs = (
	('fixed'   , 'Fixed Tonnage'),
	('jumpjet' , 'Jumpjet'),
	('masc'    , 'MASC'),
	('melee'   , 'Melee Weapon'),
        ('fraction', 'Fraction of Unit Tonnage'),
	('armour'  , 'Armour'),
	('engine'  , 'Engine'),
	('gyro'    , 'Gyro'),
	('structure', 'Internal Structure'),
	('targetting_computer', 'Targetting Computer'),
	('supercharger', 'Supercharger'),
        ('retractable', 'Retractable Blade'),
        ('turret','Mech Turret'),
)

def fixed(self, mech=None, units=None, location=None):
    return self.tonnage_factor

def jumpjet(self, mech=None, units=None, location=None):
    if mech.tonnage <= 55:
        return Decimal(0.5) * self.tonnage_factor
    if mech.tonnage > 55 and mech.tonnage <= 85:
        return self.tonnage_factor
    else:
        #90+ Tons
        return Decimal(2.0) * self.tonnage_factor 
    
def masc(self, mech=None, units=None, location=None):
    return ceil( mech.tonnage * 0.05 )

def melee(self, mech=None, units=None, location=None):
    return ceil( mech.tonnage / self.tonnage_factor )

def fraction(self, mech=None, units=None, location=None):
    return half_ton(mech.tonnage / self.tonnage_factor)

def armour(self, mech=None, units=None, location=None):
    if units == None:
        units = mech.total_armour()
    
    return half_ton(units / (self.tonnage_factor * 16))

def engine(self, mech=None, units=None, location=None):
    #FIXME: Should lookup tonnage in tables
    return None
   
def structure(self, mech=None, units=None, location=None):
    return half_ton((mech.tonnage * self.tonnage_factor) / 10)
    
def gyro(self, mech=None, units=None, location=None):
    return Decimal(ceil(mech.engine_rating / 100.0)) * self.tonnage_factor 
   
def targetting_computer(self, mech=None, units=None, location=None):
    return ceil(mech.directfire_tonnage() / Decimal(4.0))
   
def supercharger(self, mech=None, units=None, location=None):
    #FIXME: Should be Engine Tonnage / 10
    return None

def retractable(self, mech=None, units=None, location=None):
    return half_ton(mech.tonnage / self.tonnage_factor) + 0.5

def turret(self, mech=None, units=None, location=None):
    if location != None:
        return half_ton(location.location.turret_tonnage() / 10.0)
    else:
        #FIXME: This could be a pain in the arse....
        return None
            
