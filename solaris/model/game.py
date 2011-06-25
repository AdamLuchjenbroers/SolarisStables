from django.db import models
from math import ceil

class Mech(models.Model):
  value = models.IntegerField
  tonnage = models.IntegerField
  move_walk = models.IntegerField
  mech_name = models.CharField(max_length=25)
  mech_code = models.CharField(max_length=10)
  
  def engine_rating():
    return move_walk * tonnage
    
  def gyro_tonnage():
    return ceil(engine_rating / 100)
  
  def move_run():
    return ceil(move_walk * 1.5)
    
class Stable(models.Model):
  StableName = models.CharField(max_length=200)
  login = models.CharField(max_length=20)
  Reputation = models.IntegerField()
  
class StableMech(models.Model):
  owner_stable = models.ForeignKey(solaris.model.Stable)
  mech_type = models.ForeignKey(solaris.model.Mech)
  value = models.IntegerField
  
  