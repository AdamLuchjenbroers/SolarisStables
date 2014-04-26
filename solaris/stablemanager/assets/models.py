from django.db import models
from solaris.stablemanager.models import Stable
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.pilotskill.models import PilotAbility


class Pilot(models.Model):
    pilot_validRanks = (
                   ('R', 'Rookie')    ,
                   ('C', 'Contender') ,
                   ('S', 'Star')      ,
                   ('X', 'Champion')  ,
                   )
    
    stable = models.ForeignKey(Stable, blank=True)
    pilot_name = models.CharField(max_length=50, blank=True)
    pilot_callsign = models.CharField(max_length=20)
    pilot_rank = models.CharField(max_length=1, choices=pilot_validRanks)
    skill_gunnery = models.IntegerField()
    skill_pilotting = models.IntegerField()
    exp_character_points = models.IntegerField(default=0)
    exp_wounds = models.IntegerField()
    skill = models.ManyToManyField(PilotAbility, blank=True, through='PilotTraining')
    
    def isDead(self):
        return (self.exp_wounds >= 6)
        
    class Meta:
        verbose_name_plural = 'Pilots'
        verbose_name = 'Pilot'
        db_table = 'stablemanager_pilot'
        app_label = 'stablemanager'
        
    def __unicode__(self):
        return self.pilot_callsign
    
class PilotTraining(models.Model):
    pilot = models.ForeignKey(Pilot)
    training = models.ForeignKey(PilotAbility)
    notes = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'stablemanager_pilottraining'
        app_label = 'stablemanager'    
            
class Mech(models.Model):
    stable = models.ForeignKey(Stable, blank=True, null=True)
    mech_type = models.ForeignKey(MechDesign)
    signature_of = models.ForeignKey(Pilot, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Mechs'
        verbose_name = 'Mech'
        db_table = 'stablemanager_mech'
        app_label = 'stablemanager'
