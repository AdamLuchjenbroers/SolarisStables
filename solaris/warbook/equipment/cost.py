
cost_funcs = (
	('fixed'   , 'Fixed Cost'),
	('per_ton' , 'Per Ton'),
)

def fixed(self, mech, units=None):
    return self.cost_factor

def per_ton(self, mech, units=None):
    return self.cost_factor * self.tonnage()
