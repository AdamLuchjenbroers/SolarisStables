from django.db import models
from math import ceil

from .refdata import locations_all


class MechDesign(models.Model):
    mech_name = models.CharField(max_length=100)
    mech_code = models.CharField(max_length=50)
    stock_design = models.BooleanField(default=True)
    credit_value = models.IntegerField()
    bv_value = models.IntegerField()
    tonnage = models.IntegerField()
    move_walk = models.IntegerField()
    is_omni = models.BooleanField(default=False)
    omni_basechassis = models.ForeignKeyField(MechDesign, null=True)
    ssw_filename = models.CharField(max_length=1024, blank=True, null=True, unique=True)
 
    def engine_rating(self):
        return self.move_walk * self.tonnage
  
    def gyro_tonnage(self):
        return ceil(self.engine_rating / 100) 
  
    def move_run(self):
        return ceil(self.move_walk * 1.5)

    class Meta:
        unique_together = (('mech_name', 'mech_code'),)
        verbose_name_plural = 'Mech Designs'
        verbose_name = 'Mech Design'
        db_table = 'warbook_mechdesign'
        app_label = 'warbook'
        
    def __unicode__(self):
        return '%s %s' % (self.mech_name, self.mech_code)

class MechLocation(models.Model):
    location = models.CharField(max_length=3, unique=True, choices=locations_all)
    criticals = models.IntegerField()
    rear_of = models.ForeignKeyField(MechLocation, null=True)
    
class MechDesignLocation(models.Model):
    mech = models.ForeignKeyField(MechDesign)
    location = models.ForeignKeyField(MechLocation)
    armor = models.IntegerField()
    structure = models.IntegerField(null=True)