from django.db import models
from genshi import Markup

class Technology(models.Model):
  name = models.CharField(max_length=40)
  urlname = models.CharField(max_length=20)
  description = models.TextField()
  base_difficulty = models.IntegerField()
  tier = models.IntegerField()
  show = models.BooleanField()
 
  def __unicode__(self):
    return self.name

class TechnologyRollModifier(models.Model):
  technology = models.ForeignKey(Technology)
  modifier   = models.IntegerField(default=2)
  condition  = models.CharField(max_length=120)