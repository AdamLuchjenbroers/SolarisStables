from types import MethodType

from django.db import models

from solaris.warbook.mech.models import MechDesign, MechDesignLocation
from solaris.warbook.equipment import tonnage, criticals, cost

class Equipment(models.Model):
    name = models.CharField(max_length=100, default='FIXME')
    ssw_name = models.CharField(max_length=100, unique=True)
    tonnage_func = models.CharField(max_length=40, choices=tonnage.tonnage_funcs, null=True)
    tonnage_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    critical_func = models.CharField(max_length=40, choices=criticals.critical_funcs, null=True)
    critical_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cost_func = models.CharField(max_length=40, choices=cost.cost_funcs, null=True)
    cost_factor = models.DecimalField(max_digits=16, decimal_places=4, null=True)
    
    # Can this item be split across multiple locations
    splittable = models.BooleanField(default=False)
    # Can this equipment take critical hits
    crittable = models.BooleanField(default=True)
    
    # Is this item a weapon that uses ammo
    has_ammo = models.BooleanField(default=False)
    # Is this item the basic ammo type for its launcher
    basic_ammo = models.BooleanField(default=False)
    ammo_for = models.ForeignKey('Equipment', null=True, blank=True)
    ammo_size = models.IntegerField(null=True,blank=True)
    weapon_properties = models.CharField(max_length=20, null=True, blank=True)
    # Are the tonnage / criticals for this item only derivable after the rest of the mech is loaded
    evaluate_last = models.BooleanField(default=False)    
    
    record_states = (
        (0, 'Aggressive Load')
    ,   (1, 'Incomplete')
    ,   (2, 'Completed')
    )
    record_status = models.IntegerField(choices=record_states, default=0)
    
    equipment_classes = (
           ('E', 'Engine'),
           ('G', 'Gyro'),
           ('C', 'Cockpit & Systems'),
           ('W', 'Weapon'),
           ('H', 'Heatsink'),
           ('J', 'Jumpjet'),
           ('Q', 'Equipment'),
           ('S', 'Armour / Structure'),
           ('A', 'Ammunition'),
           ('T', 'Actuator'),
           ('M', 'Mission Items'),
           ('?', 'Unclassified'),
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
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return '<%s>' % self.ssw_name
            
    class Meta:
        verbose_name_plural = 'Equipment'
        verbose_name = 'Equipment'
        db_table = 'warbook_equipment'
        app_label = 'warbook'
        
        ordering = ['equipment_class', 'name']
        

class MechEquipment(models.Model):
    mech = models.ForeignKey(MechDesign, related_name='loadout')
    equipment = models.ForeignKey(Equipment)
    
    def criticals(self):
        crit_count = 0
        if self.mountings:
            for location in self.mountings.all():
                crit_count += location.num_slots()
        
        return crit_count
    
    def delete(self):
        for mount in self.mountings.all():
            mount.delete()
        super(MechEquipment,self).delete()
        
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
    rear_firing = models.BooleanField(default=False)
    turret_mounted = models.BooleanField(default=False)
    
    def get_equipmentname(self):
        return self.equipment.equipment.name
    
    def get_slots(self):
        return self.slots.split(',')
        
    def set_slots(self, slots):
        self.slots = ','.join(slots)
        
    def num_slots(self):
        return len(self.get_slots())
    
    def is_crittable(self):
        return self.equipment.equipment.crittable
    
        
    class Meta:
        verbose_name_plural = 'Mounting'
        verbose_name = 'Mounting'
        db_table = 'warbook_mechmounting'
        app_label = 'warbook'
