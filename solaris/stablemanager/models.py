from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
        
    def remaining_tasks(self):
        #STUB: Will return a list of incomplete data (e.g. missing repair
        #bills, unspent training points, etc).
        return None
    
    def current_balance(self):
        try:
            ledger = self.ledger.get(week=self.current_week)
            return ledger.closing_balance()
        except ObjectDoesNotExist:
            return 0
    
    def week_complete(self):
        return (self.remaining_tasks == None and self.current_week.next_week != None)
     

