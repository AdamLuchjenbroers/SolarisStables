
tonnage_funcs = (
	('Fixed Tonnage', 'fixed'),
	('Jumpjet', 'jumpjet'),
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