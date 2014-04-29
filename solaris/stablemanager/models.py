from django.db import models
from django.contrib.auth.models import User
from solaris.warbook.models import House
from solaris.warbook.techtree.models import Technology
from solaris.warbook.pilotskill.models import PilotDiscipline
from solaris.battlereport.models import BroadcastWeek
  
class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, null=True)
    house = models.ForeignKey(House, null=True)
    reputation = models.IntegerField()
    supply_contract = models.ManyToManyField(Technology)
    stable_disciplines = models.ManyToManyField(PilotDiscipline)
    current_week = models.ForeignKey(BroadcastWeek, null=True)
    
    def __unicode__(self):
        return self.stable_name

