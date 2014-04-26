from django.db import models
from math import ceil


class MechDesign(models.Model):
    mech_name = models.CharField(max_length=25)
    mech_code = models.CharField(max_length=10)
    stock_design = models.BooleanField(default=True)
    credit_value = models.IntegerField()
    bv_value = models.IntegerField()
    tonnage = models.IntegerField()
    move_walk = models.IntegerField()
    is_omni = models.BooleanField(default=False)
    ssw_filename = models.CharField(max_length=255, blank=True, null=True)
 
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
