
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from solaris.stablemanager.models import Stable, StableWeek
from solaris.warbook.pilotskill.models import PilotTrait, PilotRank, TrainingCost
from solaris.warbook.models import House

    
class Pilot(models.Model):    
    stable = models.ForeignKey(Stable, blank=True, related_name='pilots')
    pilot_name = models.CharField(max_length=50, blank=True)
    pilot_callsign = models.CharField(max_length=20)
    affiliation = models.ForeignKey(House)
    is_active = models.BooleanField(default=True)
        
    class Meta:
        verbose_name_plural = 'Pilots'
        verbose_name = 'Pilot'
        db_table = 'stablemanager_pilot'
        app_label = 'stablemanager'
        
        unique_together = ('stable', 'pilot_callsign')
        
    def __unicode__(self):
        if self.pilot_name != "":
            try:
                (first, last) = self.pilot_name.split(' ',1)
                return '%s \"%s\" %s' % (first, self.pilot_callsign, last)
            except ValueError:
                return '%s AKA \"%s\"' % (self.pilot_name, self.pilot_callsign)
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
    
class PilotWeekTraits(models.Model):
    pilot_week = models.ForeignKey('PilotWeek')
    trait = models.ForeignKey(PilotTrait)
    notes = models.CharField(max_length=50, blank=True, null=True)
    
    def skill(self):
        return self.__unicode__()
    
    def __unicode__(self):
        if self.notes:
            return '%s (%s)' % (self.trait.name, self.notes)
        else:
            return self.trait.name
    
    class Meta:
        db_table = 'stablemanager_pilotweektraits'
        app_label = 'stablemanager'   
    
class PilotWeek(models.Model):
    pilot = models.ForeignKey(Pilot, related_name='weeks')
    week = models.ForeignKey(StableWeek, related_name='pilots')
    
    start_character_points = models.IntegerField(default=0)
    adjust_character_points = models.IntegerField(default=0)
    
    assigned_training_points = models.IntegerField(default=0)
        
    rank = models.ForeignKey(PilotRank)
    skill_gunnery = models.IntegerField(default=5)
    skill_piloting = models.IntegerField(default=6)
    wounds = models.IntegerField(default=0)
    wounds_set = models.BooleanField(default=False)
    fame = models.IntegerField(default=0)
    fame_set = models.BooleanField(default=False)
    
    traits = models.ManyToManyField(PilotTrait, blank=True, through=PilotWeekTraits)
    next_week = models.OneToOneField('PilotWeek', on_delete=models.SET_NULL, related_name='prev_week', blank=True, null=True)
    
    def is_dead(self):
        return (self.wounds >= 6)

    def set_wounds(self, wounds, direct=True):
        self.wounds = wounds
        if direct:
            self.wounds_set = True
        self.save()

        if self.next_week != None and self.next_week.wounds_set == False and wounds > 1:
            self.next_week.set_wounds(wounds-1, direct=False)

    def set_fame(self, fame, direct=True):
        self.fame = fame
        if direct:
            self.fame_set = True
        self.save()

        if self.next_week != None and self.next_week.fame_set == False:
            self.next_week.set_fame(fame, direct=False)

    def advance(self):
        if self.week.next_week == None:
            return None
        
        if self.next_week != None:
            return self.next_week

        try:
            # Try to get the next week along after this one, in case it already exists
            # Should rarely return anything, but this is included as a safety feature
            self.next_week = PilotWeek.objects.get(pilot=self.pilot, week=self.week.next_week)
            self.save()
            return self.next_week
        except ObjectDoesNotExist:
            pass
 
        self.next_week = PilotWeek.objects.create(
          pilot = self.pilot
        , week = self.week.next_week 
        , start_character_points = self.character_points()
        , wounds = max(self.wounds - 1, 0)
        , rank = self.rank
        , fame = self.fame
        )
        self.save()

        pilot_training = self.training.filter(training__training='P')
        if pilot_training.count() > 0:
            self.next_week.skill_piloting = pilot_training.aggregate(models.Min('training__train_to'))['training__train_to__min'] 
        else:
            self.next_week.skill_piloting = self.skill_piloting 

        gunnery_training = self.training.filter(training__training='G')
        if gunnery_training.count() > 0:
            self.next_week.skill_gunnery = gunnery_training.aggregate(models.Min('training__train_to'))['training__train_to__min'] 
        else:
            self.next_week.skill_gunnery = self.skill_gunnery 
        
        for trait in self.traits.all():
            PilotWeekTraits.objects.create(
               pilot_week = self.next_week
            ,  trait = trait.trait
            ,  notes = trait.notes
            )
        # TODO: Parse training events to add any new skills.
        self.next_week.save()
        return self.next_week
        
    class Meta:
        db_table = 'stablemanager_pilotweek'
        app_label = 'stablemanager' 

        ordering = ['rank__id', 'skill_gunnery', 'skill_piloting', 'pilot__pilot_callsign']

    def training_cost(self):
        #TODO: Sum up training costs
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
        
        skills_bv = self.traits.aggregate( models.Sum('bv_mod'))['bv_mod__sum']
        if skills_bv != None:
            base_bv += float(skills_bv)

        return base_bv

    def bv_formatted(self):
        return '%0.2f' % self.bv()
        
    
class PilotTrainingEvent(models.Model):
    pilot_week = models.ForeignKey('PilotWeek', related_name='training')
    training = models.ForeignKey(TrainingCost)
    notes = models.CharField(max_length=50, blank=True, null=True)
        
    class Meta:
        db_table = 'stablemanager_trainingevent'
        app_label = 'stablemanager'   
