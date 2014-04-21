from django.db import models
from django.contrib.auth.models import User
from math import ceil

'''
class Mech(models.Model):
    mech_name = models.CharField(max_length=25)
    mech_code = models.CharField(max_length=10)
    value = models.IntegerField()
    tonnage = models.IntegerField()
    move_walk = models.IntegerField()
 
    def engine_rating(self):
        return self.move_walk * self.tonnage
  
    def gyro_tonnage(self):
        return ceil(self.engine_rating / 100) 
  
    def move_run(self):
        return ceil(self.move_walk * 1.5)
'''
  
class Stable(models.Model):
    StableName = models.CharField(max_length=200)
    Owner = models.OneToOneField(User)
    Reputation = models.IntegerField()
    
    def __unicode__(self):
        return self.StableName

'''  
class StableMech(models.Model):
    owner_stable = models.ForeignKey(Stable)
    mech_type = models.ForeignKey(Mech)
    value = models.IntegerField()
'''
