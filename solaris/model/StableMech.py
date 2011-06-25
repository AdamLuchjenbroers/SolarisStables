from django.db import models

class StableMech(models.Model):
  owner_stable = models.ForeignKey(solaris.model.Stable)
  mech_type = models.ForeignKey(solaris.model.Mech)
  value = models.IntegerField
  
  