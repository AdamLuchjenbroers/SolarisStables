
from django.db import models

from solaris.stablemanager.models import Stable, StableWeek
from solaris.stablemanager.ledger.models import LedgerItem

class StableMechManager(models.Manager):
    def create_mech(self, stable=None, purchased_as=None, purchased_on=None, create_ledger=True):
        stablemech = StableMech.objects.create(stable=stable, purchased_as=purchased_as)
        
        stablemechweek = StableMechWeek.objects.create(
          stableweek = purchased_on
        , stablemech = stablemech
        , current_design = purchased_as
        )
        
        if create_ledger:
            self.ledgeritem = LedgerItem.objects.create (
              ledger = purchased_on
            , description = 'Purchase - %s' % purchased_as.__unicode__()
            , cost = -purchased_as.credit_value
            , type = 'P'
            , tied = True
            , ref_mechdesign = purchased_as
            , ref_stablemech = stablemech
            , ref_stablemech_week = stablemechweek
            )

        return stablemech
           
class StableMech(models.Model):
    stable = models.ForeignKey(Stable, blank=True, null=True)
    purchased_as = models.ForeignKey('warbook.MechDesign')
    
    objects = StableMechManager()

    class Meta:
        verbose_name_plural = 'Mechs'
        verbose_name = 'Mech'
        db_table = 'stablemanager_mech'
        app_label = 'stablemanager'

class StableMechWeekManager(models.Manager):
    use_for_related_fields = True

    def non_signature(self):
        return self.filter(signature_of=None).order_by('current_design__tonnage', 'current_design__mech_name')

class StableMechWeek(models.Model):
    stableweek = models.ForeignKey(StableWeek, related_name='mechs', blank=True, null=True)
    stablemech = models.ForeignKey(StableMech, related_name='weeks')
    current_design = models.ForeignKey('warbook.MechDesign')
    signature_of = models.ForeignKey('Pilot', related_name='signature_mechs', blank=True, null=True)

    objects = StableMechWeekManager()
    
    class Meta:
        db_table = 'stablemanager_mechweek'
        app_label = 'stablemanager'
