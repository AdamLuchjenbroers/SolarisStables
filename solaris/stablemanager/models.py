from django.db import models
from django.contrib.auth.models import User

  
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
