from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
    
    """ These fields can optionally be used to link tied Ledger Items to their source events """
    ref_mechdesign = models.ForeignKey('warbook.MechDesign', blank=True, null=True)
    ref_stablemech = models.ForeignKey('StableMech', blank=True, null=True)
    ref_stablemech_week = models.ForeignKey('StableMechWeek', blank=True, null=True)
    ref_repairbill = models.OneToOneField('RepairBill', blank=True, null=True, related_name='ledger')
    ref_pilot = models.ForeignKey('Pilot', blank=True, null=True)
    ref_pilot_week = models.ForeignKey('PilotWeek', blank=True, null=True)
    
    def get_cost(self):
        #Use a method for this so implementing repairbills / winnings will be smoother in future.
        return self.cost
    
    class Meta:
        verbose_name_plural = 'StableWeek Items'
        verbose_name = 'StableWeek Item'
        db_table = 'stablemanager_ledgeritem'
        app_label = 'stablemanager'

@receiver(post_save, sender=LedgerItem)
def recalculate_ledgers(sender, instance=None, created=False, **kwargs):
    instance.ledger.recalculate()

@receiver(post_delete, sender=LedgerItem)
def recalculate_ledgers_ondelete(sender, instance=None, created=False, **kwargs):
    instance.ledger.recalculate()
