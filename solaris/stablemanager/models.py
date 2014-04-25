from django.db import models
from django.contrib.auth.models import User
from solaris.warbook.techtree.models import Technology
  
class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, null=True)
    reputation = models.IntegerField()
    supply_contract = models.ManyToManyField(Technology)
    
    def __unicode__(self):
        return self.stable_name

