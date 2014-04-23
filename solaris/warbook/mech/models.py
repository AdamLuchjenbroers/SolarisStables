from django.db import models
from math import ceil


class MechDesign(models.Model):
    mech_name = models.CharField(max_length=25)
    mech_code = models.CharField(max_length=10)
    stock_design = models.BooleanField()
    value = models.IntegerField()
    tonnage = models.IntegerField()
    move_walk = models.IntegerField()
 
    def engine_rating(self):
        return self.move_walk * self.tonnage
  
    def gyro_tonnage(self):
        return ceil(self.engine_rating / 100) 
  
    def move_run(self):
        return ceil(self.move_walk * 1.5)

    class Meta:
        unique_together = (('mech_name', 'mech_code'),)
