from django.db import models
from solaris.battlereport.models import BroadcastWeek
from solaris.stablemanager.models import Stable


class Ledger(models.Model):
    stable = models.ForeignKeyField(Stable)
    week = models.ForeignKeyField(BroadcastWeek)
    opening_balance = models.IntegerField()
    
    class Meta:
        verbose_name_plural = 'Ledgers'
        verbose_name = 'Ledger'
        db_table = 'stablemanager_ledger'
        app_label = 'stablemanager'
    

class LedgerItem(models.Model)
    
    item_types = (
                   ('R', 'Repair Bill')
                 , ('P'. 'Purchase')
                 , ('W', 'Winnings')
                 , ('M'. 'Misc')
                 ,)
    
    ledger = models.ForeignKeyField(Ledger)
    description = models.CharField(max_length=40)
    cost = models.IntegerField()
    type = model.CharField(max_length=1, choices=item_types)
    
    class Meta:
        verbose_name_plural = 'Ledger Items'
        verbose_name = 'Ledger Item'
        db_table = 'stablemanager_ledgeritem'
        app_label = 'stablemanager'

    