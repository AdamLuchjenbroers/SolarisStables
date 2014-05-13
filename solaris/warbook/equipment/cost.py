
cost_funcs = (
	('Fixed Cost', 'fixed'),
	('Per Ton', 'per_ton'),
)

def fixed(self, mech, units=None):
    return self.cost_factor

def per_ton(self, mech, units=None):
	return self.cost_factor * self.tonnage()
