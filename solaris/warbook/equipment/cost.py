
cost_funcs = (
	('fixed'   , 'Fixed Cost'),
	('per_ton' , 'Per Ton'),
	('engine'  , 'Engine'),
	('gyro'    , 'Gyro'),
	('mech'    , 'Mech Tonnage'),
	('jumpjet' , 'Jumpjet'),
	('per_er'  , 'By Engine Rating')
)

def fixed(self, mech, units=None):
    return self.cost_factor

def per_ton(self, mech, units=None):
    return self.cost_factor * self.tonnage()
   
def engine(self, mech):
    return (self.cost_factor * mech.tonnage * mech.engine_rating) / 75

def gyro(self, mech):
    return self.cost_factor * self.tonnage()
   
def mech(self, mech):
    return mech.tonnage * self.cost_factor
   
def jumpjet(self, mech):
    return mech.jumping_mp() * mech.tonnage * self.cost_factor
   
def per_er(self, mech):
    return self.cost_factor * mech.engine_rating
