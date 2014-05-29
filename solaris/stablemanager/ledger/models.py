from django.db import models
from solaris.battlereport.models import BroadcastWeek
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
    
    class Meta:
        verbose_name_plural = 'Ledgers'
        verbose_name = 'Ledger'
        db_table = 'stablemanager_ledger'
        app_label = 'stablemanager'
    

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

    
