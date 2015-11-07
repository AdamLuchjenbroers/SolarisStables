from django.db import models

from solaris.stablemanager.models import StableWeek
   

class LedgerItem(models.Model):
    """ A LedgerItem stores a single income or expenditure line item as part of a StableWeek """    
    item_types = (
                   ('R', 'Repair Bill')
                 , ('P', 'Purchase')
                 , ('E', 'Other Expenses')
                 , ('W', 'Winnings')
                 , ('I', 'Other Income')
                 ,)
    
    ledger = models.ForeignKey(StableWeek, related_name='entries')
    description = models.CharField(max_length=40)
    cost = models.IntegerField()
    type = models.CharField(max_length=1, choices=item_types)
    
    """ A tied LedgerItem derives its cost from a linked event or item (e.g. a repair bill) and cannot be edited directly. """
    tied = models.BooleanField(default=False)
    
    
    
    def get_cost(self):
        #Use a method for this so implementing repairbills / winnings will be smoother in future.
        return self.cost
    
    class Meta:
        verbose_name_plural = 'StableWeek Items'
        verbose_name = 'StableWeek Item'
        db_table = 'stablemanager_ledgeritem'
        app_label = 'stablemanager'

