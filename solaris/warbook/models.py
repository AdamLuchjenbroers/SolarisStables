from django.db import models
from genshi import Markup

class Technology(models.Model):
  categories = (
     ('weap' , 'Weaponry'),
     ('equip', 'Equipment'),
     ('cons' , 'Construction'),
     ('ammo' , 'Ammunition'),
   )
   
  tiers = (
    ( 0 , 'Base Technology'),
    ( 1 , 'Star-League'),
    ( 2 , 'Advanced'),
    ( 3 , 'Experimental'),
  )
  
  name = models.CharField(max_length=40)
  category = models.CharField(max_length=8, choices=categories)
  urlname = models.CharField(max_length=20)
  description = models.TextField()
  base_difficulty = models.IntegerField()
  tier = models.IntegerField(choices=tiers)
  show = models.BooleanField(default=True)
 
  def __unicode__(self):
    if self.show:
      return self.name
    else:
      return '%s (Hidden)' % self.name
   
  class Meta:
    verbose_name_plural = 'Technologies'

class TechnologyRollModifier(models.Model):
  technology = models.ForeignKey(Technology)
  modifier   = models.IntegerField(default=2)
  condition  = models.CharField(max_length=120)