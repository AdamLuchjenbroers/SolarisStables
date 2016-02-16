from decimal import Decimal

def engine_cost(oldmech, newmech):
    (oldengine, oldrating) = oldmech.get_engine_info()
    (newengine, newrating) = newmech.get_engine_info()

    if (oldengine != newengine or oldrating != newrating):
        return newengine.cost(newmech)
    else:
        return 0

def gyro_cost(oldmech, newmech):
    (oldgyro, oldtons) = oldmech.get_gyro_info()
    (newgyro, newtons) = newmech.get_gyro_info()

    if (oldgyro != newgyro or oldtons != newtons):
        return newgyro.cost(newmech)
    else:
        return 0

def armour_cost(oldmech, newmech):
    (oldarmour, oldunits) = oldmech.get_armour_info()
    (newarmour, newunits) = newmech.get_armour_info()

    if oldarmour != newarmour:
        return newarmour.cost(newmech, units=newunits)
    elif oldunits < newunits:
        return newarmour.cost(newmech, units=newunits-oldunits)
    else:
        return 0

def structure_cost(oldmech, newmech):
    # TODO
    return 0

def refit_cost(oldmech, newmech):
    parts_cost = 0

    parts_cost += engine_cost(oldmech, newmech)
    parts_cost += gyro_cost(oldmech, newmech)
    parts_cost += armour_cost(oldmech, newmech)
    parts_cost += structure_cost(oldmech, newmech)

    oldequip = oldmech.equipment_manifest()
    newequip = newmech.equipment_manifest()
    for (equipment, count) in newequip.items():
        qty = 0
        if equipment not in oldequip:
            qty = count  
        elif oldequip[equipment] < count:
            qty = count - oldequip[equipment]

        #FIXME: Location sensitive mountings
        parts_cost += (equipment.cost(newmech) * qty)

    tonnage_factor = Decimal(1.0 + (newmech.tonnage / 100.0))
    return int(parts_cost * tonnage_factor)    
