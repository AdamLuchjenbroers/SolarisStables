from django.db import models
from genshi import Markup

class Technology(models.Model):
  categories = (
     ('weap' , 'Weaponry'),
     ('equip', 'Equipment'),
     ('cons' , 'Construction'),
     ('ammo' , 'Ammunition'),
     ('phys' , 'Physical Weapons'),
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
  
  
class PilotDiscipline(models.Model):
  name  = models.CharField(max_length=40)
  blurb = models.TextField()  
  urlname = models.CharField(max_length=20)
  
  class Meta:
    verbose_name_plural = 'Pilot Disciplines'
    verbose_name = 'Pilot Discipline'

  def __unicode__(self):
    return self.name
  
class PilotAbility(models.Model):
  bv_modifiers = (
    (0.00, 'No Modifier'    ),
    (0.05, 'Piloting Skill' ),
    (0.20, 'Gunnery Skill'  ),
  )
    
  name  = models.CharField(max_length=40)
  description = models.TextField()
  discipline = models.ForeignKey(PilotDiscipline)
  bv_mod = models.DecimalField(max_digits=6 ,decimal_places=3 ,choices=bv_modifiers)
  
  def __unicode__(self):
    return self.name
 