from types import MethodType

from django.db import models

from solaris.warbook.mech.models import MechDesign, MechDesignLocation
from solaris.warbook.equipment import tonnage, criticals, cost

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    ssw_name = models.CharField(max_length=100, unique=True)
    tonnage_func = models.CharField(max_length=40, choices=tonnage.tonnage_funcs, null=True)
    tonnage_factor = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    critical_func = models.CharField(max_length=40, choices=criticals.critical_funcs, null=True)
    critical_factor = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    cost_func = models.CharField(max_length=40, choices=cost.cost_funcs, null=True)
    cost_factor = models.DecimalField(max_digits=12, decimal_places=1, null=True)
    
    # Can this item be split across multiple locations
    splittable = models.BooleanField(default=False)
    # Can this equipment take critical hits
    crittable = models.BooleanField(default=True)
    weapon_properties = models.CharField(max_length=20, null=True)
    
    equipment_classes = (
           ('Engine', 'E'),
           ('Gyro', 'G'),
           ('Cockpit & Systems', 'C'),
           ('Weapon', 'W'),
           ('Heatsink', 'H'),
           ('Jumpjet', 'J'),
           ('Equipment', 'X'),
           ('Armour / Structure', 'A'),
           ('Unclassified', '?'),
    )
    equipment_class = models.CharField(max_length=1, choices=equipment_classes, default='?')
    
    def has_weapon_property(self, w_property):
        if self.weapon_properties == None:
            return False
        
        if self.equipment_class != 'W':
            return False
        
        return w_property in self.weapon_properties.split(',')
        
    def is_directfire(self):
        return (self.has_weapon_property('DB') or self.has_weapon_property('DE'))
    
    
    def __init__(self, *args, **kwargs):
        super(Equipment, self).__init__(*args, **kwargs)
        if self.tonnage_func != None:
            self.tonnage = MethodType(getattr(tonnage, self.tonnage_func), self)
        
        if self.critical_func != None:
            self.criticals = MethodType(getattr(criticals, self.critical_func), self)
        
        if self.cost_func != None:
            self.cost = MethodType(getattr(cost, self.cost_func), self)
            
    def repair_cost(self, mech, hits):
        return self.cost(mech) * (hits / self.criticals(mech))
            
    class Meta:
        verbose_name_plural = 'Equipment'
        verbose_name = 'Equipment'
        db_table = 'warbook_equipment'
        app_label = 'warbook'
        

class MechEquipment(models.Model):
    mech = models.ForeignKey(MechDesign, related_name='loadout')
    equipment = models.ForeignKey(Equipment)
    
    def criticals(self):
        crit_count = 0
        if self.mountings:
            for location in self.mountings.all():
                crit_count += location.num_slots()
        
        return crit_count
        
    def is_directfire(self):
        return self.equipment.is_directfire()
        
    def tonnage(self):
        return self.equipment.tonnage(self.mech)
        
    def cost(self):
        return self.equipment.cost(self.mech)
        
    class Meta:
        verbose_name_plural = 'Mech Equipment'
        verbose_name = 'Mech Equipment'
        db_table = 'warbook_mechequipment'
        app_label = 'warbook'

class Mounting(models.Model):
    location = models.ForeignKey(MechDesignLocation, related_name='criticals')
    equipment = models.ForeignKey(MechEquipment, related_name='mountings') 
    # Slot allocations will be stored as a list (e.g. '2,3,4' for slots 2, 3 and 4)
    slots = models.CharField(max_length=30, blank=True)
    
    def get_slots(self):
        return self.slots.split(',')
        
    def set_slots(self, slots):
        self.slots = ','.join(slots)
        
    def num_slots(self):
        return len(self.get_slots())
    
        
    class Meta:
        verbose_name_plural = 'Mounting'
        verbose_name = 'Mounting'
        db_table = 'warbook_mechmounting'
        app_label = 'warbook'