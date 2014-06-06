from django.db import models
from django.core.urlresolvers import reverse
from math import ceil

from .refdata import locations_all, structure_entry, structure

class MechDesign(models.Model):
    mech_name = models.CharField(max_length=50)
    mech_code = models.CharField(max_length=50)
    omni_loadout = models.CharField(max_length=30, default='Base', blank=True)
    stock_design = models.BooleanField(default=True)
    credit_value = models.IntegerField(null=True)
    bv_value = models.IntegerField(null=True)
    tonnage = models.IntegerField()
    engine_rating = models.IntegerField()
    is_omni = models.BooleanField(default=False)
    omni_basechassis = models.ForeignKey('MechDesign', null=True, blank=True)
    ssw_filename = models.CharField(max_length=1024, blank=True, null=True)
    
    motive_options = (
        ('B', 'Biped')
    ,   ('Q', 'Quad')
    )    
    motive_type = models.CharField(max_length=1, choices=motive_options)
    
    techbase_options = (
        ('I', 'Inner Sphere'),
        ('C', 'Clan'),
        ('M', 'Mixed')
    )  
    tech_base = models.CharField(max_length=1, choices=techbase_options)

    production_options = (
        ('P', 'Standard Production Design'),
        ('H', 'Historical Custom Design'),
        ('C', 'Customized Stable Design')
    )
    production_type = models.CharField(max_length=1, choices=production_options, default='P')    
    
    omni_basechassis = models.ForeignKey('MechDesign', null=True, blank=True, related_name='loadouts')

    def total_armour(self):
        return (self.locations.aggregate( models.Sum('armour') ))['armour__sum']
    
    def reset_equipment(self):        
        for mount in self.loadout.all():
            mount.delete()

    def get_loadouts(self):
        if self.is_omni:
            if self.omni_basechassis:
                loadouts = [self.omni_basechassis]
                omni_loadouts = self.omni_basechassis.loadouts.all()
            else:
                loadouts = [self]
                omni_loadouts = self.loadouts.all()

            for omni_config in omni_loadouts:
                print omni_config.omni_loadout
                loadouts.append(omni_config)

            return loadouts
        else:
            return None
        
    def move_walk(self):
        return int(ceil(self.engine_rating / self.tonnage))
      
    def move_run(self):
        return int(ceil(self.move_walk() * 1.5))
       
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
        ordering = ['tonnage', 'mech_name', 'mech_code', 'omni_loadout']
        
    def __unicode__(self):
        return '%s %s' % (self.mech_name, self.mech_code)
    
    def get_absolute_url(self):
        return reverse('mech_detail', kwargs={'name': self.mech_name, 'code': self.mech_code, 'omni': self.omni_loadout})

class MechLocation(models.Model):
    location = models.CharField(max_length=3, unique=True, choices=locations_all)
    criticals = models.IntegerField()
    rear_of = models.ForeignKey('MechLocation', null=True)
    
    def structure(self, tonnage):
        table_entry = structure_entry(self.location)
        if table_entry != 'other':
            return structure[tonnage][table_entry]
        else:
            return None
    
    class Meta:
        verbose_name_plural = 'Mech Locations'
        verbose_name = 'Mech Location'
        db_table = 'warbook_mechlocation'
        app_label = 'warbook'
    
class MechDesignLocation(models.Model):
    mech = models.ForeignKey(MechDesign, related_name='locations')
    location = models.ForeignKey(MechLocation)
    armour = models.IntegerField()
    structure = models.IntegerField(null=True, blank=True)
    
    def get_criticals(self):
        crit_table = [None] * self.location.criticals
        for item in self.criticals.all():
            for slot in item.get_slots():
                crit_table[int(slot)-1] = item
        return crit_table
    
    def location_code(self):
        return self.location.location
    
    def location_name(self):
        return self.location.get_location_display()
    
    class Meta:
        unique_together = (('mech','location'),)
        verbose_name_plural = 'Mech Design Locations'
        verbose_name = 'Mech Design Location'
        db_table = 'warbook_mechdesignlocation'
        app_label = 'warbook'
