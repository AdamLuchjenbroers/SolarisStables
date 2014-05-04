from django.db import models
from math import ceil

from .refdata import locations_all

class MechDesign(models.Model):
    mech_name = models.CharField(max_length=50)
    mech_code = models.CharField(max_length=50)
    mech_key = models.CharField(max_length=100, unique=True)
    omni_loadout = models.CharField(max_length=30, default='N/A')
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
        if not self.loadout:
            return 0
        
        for item in self.loadout.all():
            if item.equipment.equipment_class == 'J':
                jump_mp += 1
        return jump_mp
        
    def directfire_tonnage(self):
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
    mech = models.ForeignKey(MechDesign, related_name='locations')
    location = models.ForeignKey(MechLocation)
    armor = models.IntegerField()
    structure = models.IntegerField(null=True)
    
    def get_criticals(self):
        crit_table = [None] * self.location.criticals
        for item in self.criticals:
            for slot in item.get_slots():
                crit_table[slot-1] = item
        return crit_table
    
    class Meta:
        unique_together = (('mech','location'),)
        verbose_name_plural = 'Mech Design Locations'
        verbose_name = 'Mech Design Location'
        db_table = 'warbook_mechdesignlocation'
        app_label = 'warbook'
    




