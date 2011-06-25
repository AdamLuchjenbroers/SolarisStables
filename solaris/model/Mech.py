from django.db import models
from math import ceil

class Mech(models.Model):
  value = models.IntegerField
  tonnage = models.IntegerField
  move_walk = models.IntegerField
  
  def engine_rating():
    return move_walk * tonnage
    
  def gyro_tonnage():
    return ceil(engine_rating / 100)
  
  def move_run():
    return ceil(move_walk * 1.5)