from math import ceil
from decimal import Decimal

cost_funcs = (
	('fixed'     , 'Fixed Cost'),
	('per_ton'   , 'Per Ton'),
	('structure' , 'Structure'),
	('engine'    , 'Engine'),
	('gyro'      , 'Gyro'),
	('mech'      , 'Mech Tonnage'),
	('jumpjet'   , 'Jumpjet'),
	('per_er'    , 'By Engine Rating'),
	('masc'      , 'MASC'),
	('retract'   , 'Retractable Blade')
)

def fixed(self, mech, units=None):
    return self.cost_factor

def per_ton(self, mech, units=None):
    return self.cost_factor * Decimal(self.tonnage(units=units))
   
def retract(self, mech, units=None):   
    return self.cost_factor * ( Decimal(self.tonnage(units=units)) + 1)
   
def structure(self, mech, units=None):
    return self.cost_factor * Decimal(ceil(units/8) / 2)
   
def engine(self, mech, units=None):
    return (self.cost_factor * mech.tonnage * mech.engine_rating) / 75

def gyro(self, mech, units=None):
    return self.cost_factor * self.tonnage(mech=mech, units=units)
   
def mech(self, mech, units=None):
    return mech.tonnage * self.cost_factor
   
def jumpjet(self, mech, units=None):
    return mech.move_jump() * mech.tonnage * self.cost_factor
   
def per_er(self, mech, units=None):
    return self.cost_factor * mech.engine_rating

def masc(self, mech, units=None):
    return self.cost_factor * mech.engine_rating * self.tonnage(mech, units=units)
