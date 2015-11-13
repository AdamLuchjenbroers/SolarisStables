
from django.db import models

from solaris.stablemanager.models import Stable, StableWeek
           
class StableMech(models.Model):
    stable = models.ForeignKey(Stable, blank=True, null=True)
    purchased_as = models.ForeignKey('warbook.MechDesign')
    signature_of = models.ForeignKey('Pilot', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Mechs'
        verbose_name = 'Mech'
        db_table = 'stablemanager_mech'
        app_label = 'stablemanager'

class StableMechWeek(models.Model):
    stableweek = models.ForeignKey(StableWeek, blank=True, null=True)
    stablemech = models.ForeignKey(StableMech)
    current_design = models.ForeignKey('warbook.MechDesign')
    signature_of = models.ForeignKey('Pilot', blank=True, null=True)
    
    class Meta:
        db_table = 'stablemanager_mechweek'
        app_label = 'stablemanager'
