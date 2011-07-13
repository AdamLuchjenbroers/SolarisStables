from django.db import models
from genshi import Markup

class Technology(models.Model):
  categories = (
     ('weap' , 'Weaponry'),
     ('equip', 'Equipment'),
     ('cons' , 'Construction'),
     ('ammo' , 'Ammunition'),
   )
  
  name = models.CharField(max_length=40)
  category = models.CharField(max_length=8, choices=categories)
  urlname = models.CharField(max_length=20)
  description = models.TextField()
  base_difficulty = models.IntegerField()
  tier = models.IntegerField()
  show = models.BooleanField(default=True)
 
  def __unicode__(self):
    if self.show:
      return self.name
    else:
      return '%s (Hidden)' % self.name

class TechnologyRollModifier(models.Model):
  technology = models.ForeignKey(Technology)
  modifier   = models.IntegerField(default=2)
  condition  = models.CharField(max_length=120)