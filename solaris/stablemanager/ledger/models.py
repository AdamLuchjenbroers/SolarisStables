from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.signals import post_save
from django.dispatch import receiver

from solaris.campaign.models import BroadcastWeek
from solaris.stablemanager.models import Stable

class Ledger(models.Model):
    stable = models.ForeignKey(Stable, related_name='ledger')
    week = models.ForeignKey(BroadcastWeek)
    opening_balance = models.IntegerField()
    next_ledger = models.ForeignKey('Ledger', null=True, related_name='prev_ledger')
    
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
            return self.objects.get(stable=self.stable, week=self.week.next_week)
        except ObjectDoesNotExist:
            pass
        
        self.next_ledger = self.objects.create(
            stable = self.stable
        ,   week = self.week.next_week
        ,   opening_balance = self.closing_balance()
        )
        self.save()
        
        return self.next_ledger
            
    def get_absolute_url(self):
        return reverse('stable_ledger', kwargs={'week': self.week.week_number})
    
    class Meta:
        verbose_name_plural = 'Ledgers'
        verbose_name = 'Ledger'
        db_table = 'stablemanager_ledger'
        app_label = 'stablemanager'
        
        unique_together = ('stable', 'week')
    

class LedgerItem(models.Model):
    """ A LedgerItem stores a single income or expenditure line item as part of a Ledger """    
    item_types = (
                   ('R', 'Repair Bill')
                 , ('P', 'Purchase')
                 , ('E', 'Other Expenses')
                 , ('W', 'Winnings')
                 , ('I', 'Other Income')
                 ,)
    
    ledger = models.ForeignKey(Ledger, related_name='entries')
    description = models.CharField(max_length=40)
    cost = models.IntegerField()
    type = models.CharField(max_length=1, choices=item_types)
    
    """ A tied LedgerItem derives its cost from a linked event or item (e.g. a repair bill) and cannot be edited directly. """
    tied = models.BooleanField(default=False)
    
    
    
    def get_cost(self):
        #Use a method for this so implementing repairbills / winnings will be smoother in future.
        return self.cost
    
    class Meta:
        verbose_name_plural = 'Ledger Items'
        verbose_name = 'Ledger Item'
        db_table = 'stablemanager_ledgeritem'
        app_label = 'stablemanager'
    

@receiver(post_save, sender=Stable)
def setup_initial_ledger(sender, created=False, **kwargs):
    if created:
        (ledger, newledger) = Ledger.objects.get_or_create(stable=sender, week=sender.current_week)
        if newledger:
            ledger.opening_balance = 75000000

        ledger.save()
