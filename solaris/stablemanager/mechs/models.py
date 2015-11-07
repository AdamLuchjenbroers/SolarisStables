
from django.db import models

from solaris.stablemanager.models import Stable, StableWeek
from solaris.warbook.mech.models import MechDesign
    
           
class StableMech(models.Model):
    stable = models.ForeignKey(Stable, blank=True, null=True)
    mech_type = models.ForeignKey(MechDesign)
    mech_name = models.CharField(max_length=20, blank=True, null=True)
    signature_of = models.ForeignKey(Pilot, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Mechs'
        verbose_name = 'Mech'
        db_table = 'stablemanager_mech'
        app_label = 'stablemanager'

class StableMechWeek(models.Model):
    stableweek = models.ForeignKey(StableWeek, blank=True, null=True)
    stablmeck = models.ForeignKey(StableMech)
    mech_name = models.CharField(max_length=20, blank=True, null=True)
    signature_of = models.ForeignKey(Pilot, blank=True, null=True)
    
    class Meta:
        db_table = 'stablemanager_mechweek'
        app_label = 'stablemanager'