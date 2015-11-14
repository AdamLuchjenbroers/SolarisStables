from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from solaris.warbook.models import House
from solaris.warbook.techtree.models import Technology
from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.campaign.models import BroadcastWeek


class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, null=True)
    house = models.ForeignKey(House, null=True)
    reputation = models.IntegerField(default=0)
    supply_contract = models.ManyToManyField(Technology)
    stable_disciplines = models.ManyToManyField(PilotTraitGroup)
    
    def __unicode__(self):
        return self.stable_name
    
    def get_stableweek(self, for_week=None):
        return self.ledger.get(next_week=for_week)
    
    def current_balance(self):
        try:
            ledger = self.get_stableweek()
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
        
     
class StableWeek(models.Model):
    stable = models.ForeignKey('Stable', related_name='ledger')
    week = models.ForeignKey(BroadcastWeek)
    opening_balance = models.IntegerField()
    next_week = models.ForeignKey('StableWeek', null=True, related_name='prev_week')
    
    def closing_balance(self):
        balance = self.opening_balance
        
        for item in self.entries.all():
            balance += item.get_cost()
            
        return balance
    
    def advance(self):
        if self.week.next_week == None:
            return
        
        try:
            # Try to get the next week along after this one, in case it already exists
            # Should rarely return anything, but this is included as a safety feature
            self.next_week = self.objects.get(stable=self.stable, week=self.week.next_week)
            self.save()
            return self.next_week
        except ObjectDoesNotExist:
            pass
        
        self.next_week = self.objects.create(
            stable = self.stable
        ,   week = self.week.next_week
        ,   opening_balance = self.closing_balance()
        )
        self.save()
        
        return self.next_week
            
    def get_absolute_url(self):
        return reverse('stable_ledger', kwargs={'week': self.week.week_number})
    
    class Meta:
        verbose_name_plural = 'Ledgers'
        verbose_name = 'StableWeek'
        db_table = 'stablemanager_stableweek'
        app_label = 'stablemanager'
        
        unique_together = ('stable', 'week')
        
    
@receiver(post_save, sender=Stable)
def setup_initial_ledger(sender, instance=None, created=False, **kwargs):
    if created:
        ledger = StableWeek.objects.create(stable=instance, week=BroadcastWeek.objects.current_week(), opening_balance=75000000 )
        ledger.save
