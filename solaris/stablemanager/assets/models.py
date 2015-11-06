
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from solaris.stablemanager.models import Stable
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.pilotskill.models import PilotTrait, PilotRank
from solaris.warbook.models import House
from solaris.battlereport.models import BroadcastWeek
    
class Pilot(models.Model):    
    stable = models.ForeignKey(Stable, blank=True, related_name='pilots')
    pilot_name = models.CharField(max_length=50, blank=True)
    pilot_callsign = models.CharField(max_length=20)
    affiliation = models.ForeignKey(House)
    is_active = models.BooleanField(default=True)
    
    def isDead(self):
        return (self.exp_wounds >= 6)
        
    class Meta:
        verbose_name_plural = 'Pilots'
        verbose_name = 'Pilot'
        db_table = 'stablemanager_pilot'
        app_label = 'stablemanager'
        
        unique_together = ('stable', 'pilot_callsign')
        
    def __unicode__(self):
        if self.pilot_name != None:
            (first, last) = self.pilot_name.split(' ',1)
            return '%s \"%s\" %s' % (first, self.pilot_callsign, last)
        else:
            return self.pilot_callsign
    
    def full_name(self):
        return self.__unicode__()
    
    def deactivate(self):
        self.is_active = False
        self.save()
    
    def advance(self, current_week):        
        try:
            pilotweek = self.weeks.get(week=current_week)
            pw = pilotweek.advance()
            if pw == None:
                self.deactivate()
        except ObjectDoesNotExist:            
            self.deactivate() # Dead or otherwise obsolete pilot
    
class PilotTraining(models.Model):
    pilot_week = models.ForeignKey('PilotWeek', related_name='skills')
    training = models.ForeignKey(PilotTrait)
    notes = models.CharField(max_length=50, blank=True, null=True)
    
    def skill(self):
        return self.__unicode__()
    
    def __unicode__(self):
        if self.notes:
            return '%s (%s)' % (self.training.name, self.notes)
        else:
            return self.training.name
    
    class Meta:
        db_table = 'stablemanager_pilottraining'
        app_label = 'stablemanager'   
    
class PilotWeek(models.Model):
    pilot = models.ForeignKey(Pilot, related_name='weeks')
    week = models.ForeignKey(BroadcastWeek)
    
    start_character_points = models.IntegerField(default=0)
    adjust_character_points = models.IntegerField(default=0)
    
    assigned_training_points = models.IntegerField(default=0)
        
    rank = models.ForeignKey(PilotRank)
    skill_gunnery = models.IntegerField(default=5)
    skill_piloting = models.IntegerField(default=6)
    wounds = models.IntegerField(default=0)
    
    skill = models.ManyToManyField(PilotTrait, blank=True, through=PilotTraining)
    
    class Meta:
        db_table = 'stablemanager_pilotweek'
        app_label = 'stablemanager'  
    
    def earned_training_points(self):
        # TODO: Derive based on battle participation
        return 0
    
    def gained_character_points(self):
        return self.adjust_character_points + self.assigned_training_points + self.rank.auto_train_cp
    
    def character_points(self):
        # TODO: Add earned character-points from battles.
        return self.start_character_points + self.gained_character_points()
    
    def bv(self):
        base_bv = 1.0
        base_bv += (4-self.skill_gunnery) * 0.20
        base_bv += (5-self.skill_piloting) * 0.05
        
        skills_bv = self.skills.aggregate( models.Sum('training__bv_mod'))['training__bv_mod__sum']
        if skills_bv != None:
            base_bv += float(skills_bv)

        return base_bv

    def bv_formatted(self):
        return '%0.2f' % self.bv()

    def advance(self):
        if self.week.next_week == None:
            return       
        
        try:
            # Try to get the next week along after this one, in case it already exists
            # Should rarely return anything, but this is included as a safety feature
            return self.objects.get(pilot=self.pilot, week=self.week.next_week)
        except ObjectDoesNotExist:
            pass
        
        # TODO - Apply Training
        new_rank = self.rank
        new_gunnery = self.skill_gunnery
        new_piloting = self.skill_piloting
        new_skill = self.skill
        
        if self.wounds > 0 and self.wounds < 6:        
            new_wounds = self.wounds - 1
        elif self.wounds == 0:
            new_wounds = self.wounds
        else:
            #Pilot is dead, and should not be advanced
            return            
        
        return PilotWeek.objects.create(
            pilot=self.pilot
        ,   week=self.week.next_week
        ,   start_character_points=self.character_points()
        ,   rank = new_rank
        ,   skill_gunnery = new_gunnery
        ,   skill_piloting = new_piloting
        ,   wounds = new_wounds
        ,   skill = new_skill
        )
            
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
