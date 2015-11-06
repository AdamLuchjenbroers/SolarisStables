from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from solaris.warbook.models import House
from solaris.warbook.techtree.models import Technology
from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.battlereport.models import BroadcastWeek


class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, null=True)
    house = models.ForeignKey(House, null=True)
    reputation = models.IntegerField(default=0)
    supply_contract = models.ManyToManyField(Technology)
    stable_disciplines = models.ManyToManyField(PilotTraitGroup)
    current_week = models.ForeignKey(BroadcastWeek, null=True)
    
    def __unicode__(self):
        return self.stable_name
        
    
    def current_balance(self):
        try:
            ledger = self.ledger.get(week=self.current_week)
            return ledger.closing_balance()
        except ObjectDoesNotExist:
            return 0
    
    def week_complete(self):
        return (self.remaining_tasks == None and self.current_week.next_week != None)
    
    def advance(self):
        """ Handles advancing the stable and all related objects to the next Broadcast Week """
        if self.current_week.next_week == None:
            return
        
        ledger = self.ledger.get(week=self.current_week)
        ledger.advance()
        
        for pilot in self.pilots.all():
            pilot.advance()        
        
     

