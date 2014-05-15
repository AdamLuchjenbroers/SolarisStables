
cost_funcs = (
	('fixed'   , 'Fixed Cost'),
	('per_ton' , 'Per Ton'),
	('engine'  , 'Engine'),
	('gyro'    , 'Gyro'),
)

def fixed(self, mech, units=None):
    return self.cost_factor

def per_ton(self, mech, units=None):
    return self.cost_factor * self.tonnage()
   
def engine(self, mech):
    return (self.cost_factor * mech.tonnage * mech.engine_rating) / 75

def gyro(self, mech):
    return self.cost_factor * self.tonnage()