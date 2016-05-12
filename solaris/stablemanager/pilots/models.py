
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

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
    pilot_week = models.ForeignKey('PilotWeek', related_name='traits')
    trait = models.ForeignKey(PilotTrait)
    notes = models.CharField(max_length=50, blank=True, null=True)
    
    def skill(self):
        return self.__unicode__()
    
    def __unicode__(self):
        if self.notes:
            return '%s (%s)' % (self.trait.name, self.notes)
        else:
            return self.trait.name

    def has_signatures(self):
        return 
    
    class Meta:
        db_table = 'stablemanager_pilotweektraits'
        app_label = 'stablemanager'  

        unique_together = [('pilot_week', 'trait')] 
    
class PilotWeek(models.Model):
    pilot = models.ForeignKey(Pilot, related_name='weeks')
    week = models.ForeignKey(StableWeek, related_name='pilots')
    
    start_character_points = models.IntegerField(default=0)
    adjust_character_points = models.IntegerField(default=0)
    
    assigned_training_points = models.IntegerField(default=0)
        
    rank = models.ForeignKey(PilotRank)
    rank_set = models.BooleanField(default=False)

    skill_gunnery = models.IntegerField(default=5)
    skill_piloting = models.IntegerField(default=6)

    wounds = models.IntegerField(default=0)
    wounds_set = models.BooleanField(default=False)
    blackmarks = models.IntegerField(default=0)
    blackmarks_set = models.BooleanField(default=False)

    fame = models.IntegerField(default=0)
    fame_set = models.BooleanField(default=False)
    
    next_week = models.OneToOneField('PilotWeek', on_delete=models.SET_NULL, related_name='prev_week', blank=True, null=True)
    
    def is_dead(self):
        return ((self.wounds + self.blackmarks) >= 6)

    def is_visible(self):
        if hasattr(self, 'prev_week'):
            if self.prev_week.is_dead():
                return False
            else:
                return self.prev_week.is_visible()
        else:
            return True    

    def is_locked(self):
        if self.next_week == None:
            # Cannot be locked if it's the most recent week.
            return False
        elif self.next_week.training.count() > 0:
            return True
        else:
            return self.next_week.is_locked()

    def set_wounds(self, wounds, direct=True):
        self.wounds = min(6,max(0,wounds))
        self.wounds_set = True
        self.save()

        return self.wounds

    def set_blackmarks(self, blackmarks, direct=True):
        self.blackmarks = min(6,max(0,blackmarks))
        self.blackmarks_set = True
        self.save()
  
        return self.blackmarks
 
    def set_fame(self, fame, direct=True):
        self.fame = fame
        self.fame_set = True
        self.save()

        return self.fame

    def advance(self):
        if self.week.next_week == None:
            return None
        
        if self.next_week != None:
            return self.next_week

        # Don't advance the record if they're dead.
        if self.is_dead():
            return None

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
        , blackmarks = self.blackmarks
        )
        self.save()

        for defer in self.deferred.all():
            defer.advance()

        self.next_week.skill_piloting = self.applied_piloting()
        self.next_week.skill_gunnery = self.applied_gunnery()

        self.copy_training()
        
        self.next_week.save()
        return self.next_week

    def copy_training(self):
        if self.next_week == None:
            return

        to_copy = (
          self.traits.all()
        , self.training.filter(training__training__in=('S','T'))
        , self.new_traits.all()
        )

        for dataset in to_copy:
            for trait in dataset:
                (new, created) = PilotWeekTraits.objects.get_or_create(
                   pilot_week = self.next_week
                ,  trait = trait.trait
                )
                new.notes = trait.notes
                new.save()
        
    class Meta:
        db_table = 'stablemanager_pilotweek'
        app_label = 'stablemanager' 

        ordering = ['rank__id', 'skill_gunnery', 'skill_piloting', 'pilot__pilot_callsign']

    def training_cost(self):
        cost = self.training.aggregate(models.Sum('training__cost'))['training__cost__sum']
        if cost != None:
            return cost
        else:
            return 0
 
    def gained_character_points(self):
        return self.adjust_character_points + self.assigned_training_points + self.rank.auto_train_cp
    
    def character_points(self):
        # TODO: Add earned character-points from battles.
        return self.start_character_points + self.gained_character_points() - self.training_cost()
    
    def bv(self):
        base_bv = 1.0
        base_bv += (4-self.skill_gunnery) * 0.20
        base_bv += (5-self.skill_piloting) * 0.05
        
        skills_bv = self.traits.aggregate( models.Sum('trait__bv_mod'))['trait__bv_mod__sum']
        if skills_bv != None:
            base_bv += float(skills_bv)

        return base_bv

    def bv_formatted(self):
        return '%0.2f' % self.bv()

    def remove_trait(self, trait):
        self.traits.filter(trait=trait).delete()

        if self.next_week != None:
            self.next_week.remove_trait(trait)

    def applied_piloting(self):
        pilot_training = self.training.filter(training__training='P')
        if pilot_training.count() > 0:
            return pilot_training.aggregate(models.Min('training__train_to'))['training__train_to__min'] 
        else:
            return self.skill_piloting 

    def next_piloting(self):
        return TrainingCost.objects.get(training='P', train_from=self.applied_piloting())

    def applied_gunnery(self):         
        gunnery_training = self.training.filter(training__training='G')
        if gunnery_training.count() > 0:
            return gunnery_training.aggregate(models.Min('training__train_to'))['training__train_to__min'] 
        else:
            return self.skill_gunnery

    def next_gunnery(self):
        return TrainingCost.objects.get(training='G', train_from=self.applied_gunnery())

    def applied_skill_count(self):
        skills = self.traits.filter(trait__discipline__discipline_type='T').count() \
               + self.training.filter(training__training='S').count()
        if skills == None:
            return 0
        else:
            return skills

    def next_skills(self):
        skills = self.applied_skill_count() 
        return TrainingCost.objects.get(training='S', train_from=skills)

    def has_discipline(self, discipline):
        if self.traits.filter(trait__discipline=discipline).count() > 0:
            return True

        if self.training.filter(trait__discipline=discipline).count() > 0:
            return True

        return False

    def week_number(self):
        return self.week.week.week_number

    def state_parcel(self):
        # Returns a basic status parcel for updating page state
        return {
          'callsign' : self.pilot.pilot_callsign
        , 'spent-xp' : self.training_cost()
        , 'final-xp' : self.character_points()
        }

    def edit_url(self):
        return reverse('stable_edit_pilot', kwargs={'week' : self.week_number(), 'callsign' : self.pilot.pilot_callsign})

    def signature_mechs(self):
        return self.pilot.signature_mechs.filter(stableweek=self.week)
    
class PilotTrainingEvent(models.Model):
    pilot_week = models.ForeignKey('PilotWeek', related_name='training')
    training = models.ForeignKey(TrainingCost)
    trait = models.ForeignKey(PilotTrait, blank=True, null=True)
    notes = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return 'Train %s [%s -> %i]' % (self.pilot_week.pilot.pilot_callsign, self.training.get_training_display(), self.training.train_to) 

    def description(self):
        if self.training.training in ('P','G'):
            return 'Upgrade %s to %i' % (self.training.get_training_display(), self.training.train_to)
        elif self.training.training == 'S':
            if self.notes != None:
                return 'Acquire %s (%s)' % (self.trait, self.notes)
            else:
                return 'Acquire %s' % self.trait
        else:
            return 'Develop %s (%s)' % (self.trait, self.notes)

    def is_locked(self):
        if self.pilot_week.is_locked():
            return True

        if self.training.training == 'P':
            return self.training.train_to != self.pilot_week.applied_piloting()
        elif self.training.training == 'G':
            return self.training.train_to != self.pilot_week.applied_gunnery()
        elif self.training.training == 'S':
            return self.training.train_to != self.pilot_week.applied_skill_count()
        else:
            return False
        
    class Meta:
        db_table = 'stablemanager_trainingevent'
        app_label = 'stablemanager'

        ordering = ('training__training', 'training__cost')
        unique_together = [('pilot_week','training'), ('pilot_week', 'trait'),]

class PilotTraitEvent(models.Model):
    pilot_week = models.ForeignKey('PilotWeek', related_name='new_traits')
    trait = models.ForeignKey(PilotTrait)
    notes = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return 'Pilot %s develops %s' % (self.pilot_week.pilot.pilot_callsign, self.trait.trait) 

    def is_locked(self):
        return self.pilot_week.is_locked()
    
    def description(self):
        if self.notes != None:
            return 'Developed %s (%s)' % (self.trait, self.notes)
        else:
            return 'Developed %s' % self.trait

    class Meta:
        db_table = 'stablemanager_traitevent'
        app_label = 'stablemanager'

        ordering = ('pilot_week__pilot__pilot_callsign', 'trait')
        unique_together = [('pilot_week', 'trait'),]

class PilotDeferment(models.Model):
    pilot_week = models.ForeignKey('PilotWeek', related_name='deferred')
    deferred = models.ForeignKey(PilotTrait)
    notes = models.CharField(max_length=50, blank=True, null=True)
    duration = models.IntegerField(default=0)
    duration_set = models.BooleanField(default=False)
    next_week = models.OneToOneField('PilotDeferment', on_delete=models.SET_NULL, related_name='prev_week', blank=True, null=True)

    def __unicode__(self):
        return '%s - %s deferred for %i weeks' % (self.pilot_week.pilot.pilot_callsign, self.deferred, self.duration) 

    def end_deferment(self):
        if hasattr(self, 'prev_week'):
            self.duration = 0
            self.duration_set = True
            self.save()
        else:
            self.cascade_delete()

    def cascade_delete(self):
        # Recursively delete this record and all following it.
        if self.next_week != None:
            self.next_week.cascade_delete()

        self.delete()

    def advance(self):
        if self.next_week != None:
            return self.next_week

        if self.pilot_week.next_week == None or self.duration <= 0:
            return None
        
        self.next_week = PilotDeferment.objects.create (
            pilot_week = self.pilot_week.next_week
        ,   deferred = self.deferred
        ,   notes = self.notes
        ,   duration = self.duration - 1
        )
        self.save()
        self.next_week.save()

    def description(self):
        if self.notes != None:
            return '%s (%s)' % (self.deferred, self.notes)
        else:
            return '%s' % self.deferred

    class Meta:
        db_table = 'stablemanager_issuedeferred'
        app_label = 'stablemanager'

        ordering = ('pilot_week__pilot__pilot_callsign', '-duration')
        unique_together = [('pilot_week', 'deferred'),]

@receiver(post_save, sender=PilotDeferment)
def cascade_deferment_update(sender, instance=None, created=False, **kwargs):
    if instance.pilot_week.next_week == None:
        return 

    if instance.next_week == None:
        instance.advance()
    elif instance.duration > 0:
        if not instance.next_week.duration_set:
            instance.next_week.duration = instance.duration - 1
            instance.next_week.save()
    else:
        instance.next_week.cascade_delete()

@receiver(post_save, sender=PilotWeek)
def perform_cascading_updates(sender, instance=None, created=False, **kwargs):
    if instance.next_week != None:
        instance.next_week.start_character_points = instance.character_points()

        if not instance.next_week.fame_set:
            instance.next_week.fame = instance.fame

        if not instance.next_week.blackmarks_set: 
            instance.next_week.blackmarks = instance.blackmarks

        if not instance.next_week.rank_set:
            instance.next_week.rank = instance.rank

        if instance.wounds > 1 and not instance.is_dead() and not instance.next_week.wounds_set:
            instance.next_week.wounds = max(0, instance.wounds-1)
        elif instance.is_dead():
            instance.next_week.wounds = 6

        instance.next_week.skill_piloting = instance.applied_piloting()
        instance.next_week.skill_gunnery = instance.applied_gunnery()

        instance.copy_training()

        instance.next_week.save()
    elif instance.week.next_week != None and not instance.is_dead():
        # There's a stableweek after this one, so advance this pilot
        instance.advance() 
