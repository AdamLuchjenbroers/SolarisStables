from django.db import models
from math import ceil

from .refdata import locations_all
import .tonnage
import .critical
import .cost

class MechDesign(models.Model):
    mech_name = models.CharField(max_length=50)
    mech_code = models.CharField(max_length=50)
    mech_key = models.CharField(max_length=100, unique=True)
    omni_loadout = models.CharField(max_length=30, default='N/A'
    stock_design = models.BooleanField(default=True)
    credit_value = models.IntegerField(null=True)
    bv_value = models.IntegerField(null=True)
    tonnage = models.IntegerField()
    engine_rating = models.IntegerField()
    is_omni = models.BooleanField(default=False)
    omni_basechassis = models.ForeignKey('MechDesign', null=True)
    ssw_filename = models.CharField(max_length=1024, blank=True, null=True)
  
    def gyro_tonnage(self):
        #FIXME: Should be handled by equipment, as this varies by gyro type
        return ceil(self.engine_rating / 100) 
        
    def move_walk(self):
        return ceil(self.engine_rating / self.tonnage)
  
    def move_run(self):
        return ceil(self.move_walk() * 1.5)
        
    def move_jump(self):
        jump_mp = 0
        if not self.loadout
            return 0
        
        for item in self.loadout.all():
            if item.equipment.equipment_class == 'J':
                jump_mp++
        return jump_mp
        
    def directfire_tonnage(self)
        tons = 0
        for item in self.loadout.all():
            if item.is_directfire():
                tons += item.tonnage()
        return tons

    class Meta:
        unique_together = (('mech_name', 'mech_code', 'omni_loadout'), ('ssw_filename', 'omni_loadout'),)
        verbose_name_plural = 'Mech Designs'
        verbose_name = 'Mech Design'
        db_table = 'warbook_mechdesign'
        app_label = 'warbook'
        
    def __unicode__(self):
        return '%s %s' % (self.mech_name, self.mech_code)

class MechLocation(models.Model):
    location = models.CharField(max_length=3, unique=True, choices=locations_all)
    criticals = models.IntegerField()
    rear_of = models.ForeignKey('MechLocation', null=True)
    
    class Meta:
        verbose_name_plural = 'Mech Locations'
        verbose_name = 'Mech Location'
        db_table = 'warbook_mechlocation'
        app_label = 'warbook'
    
class MechDesignLocation(models.Model):
    mech = models.ForeignKey(MechDesign, related_name=locations)
    location = models.ForeignKey(MechLocation)
    armor = models.IntegerField()
    structure = models.IntegerField(null=True)

    class Meta:
        unique_together = (('mech','location'),)
        verbose_name_plural = 'Mech Design Locations'
        verbose_name = 'Mech Design Location'
        db_table = 'warbook_mechdesignlocation'
        app_label = 'warbook'
        
    def get_criticals(self):
        crit_table = []
        for item in self.criticals:
            for slot in item.get_slots()
                crit_table[slot] = item
        return crit_table

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
    	   ('Heatsink', 'H').
    	   ('Jumpjet', 'J'),
    	   ('Equipment', 'X'),
    	   ('Armour / Structure', 'A'),
    	   ('Unclassified', '?'),
    )
    def equipment_class = models.CharField(max_length=1, choices=equipment_classes, default='?')
    
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
        return self.equipment.tonnage()
        
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

