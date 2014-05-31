from django.db import models
from solaris.stablemanager.models import Stable
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.pilotskill.models import PilotTrait
from solaris.warbook.models import House

class PilotRank(models.Model):
    rank = models.CharField(max_length=20, unique=True)
    min_gunnery = models.IntegerField()
    min_piloting = models.IntegerField()
    skills_limit = models.IntegerField()
    promotion = models.ForeignKey('PilotRank', null=True, blank=True)    
        
    class Meta:
        verbose_name_plural = 'Pilot Ranks'
        verbose_name = 'Pilot Rank'
        db_table = 'stablemanager_pilotrank'
        app_label = 'stablemanager'
        
    def __unicode__(self):
        return self.rank
    
class Pilot(models.Model):    
    stable = models.ForeignKey(Stable, blank=True)
    pilot_name = models.CharField(max_length=50, blank=True)
    pilot_callsign = models.CharField(max_length=20)
    pilot_rank = models.ForeignKey(PilotRank)
    skill_gunnery = models.IntegerField()
    skill_pilotting = models.IntegerField()
    exp_character_points = models.IntegerField(default=0)
    exp_wounds = models.IntegerField()
    affiliation = models.ForeignKey(House)
    skill = models.ManyToManyField(PilotTrait, blank=True, null=True, through='PilotTraining')
    
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
    training = models.ForeignKey(PilotTrait)
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
