from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils.text import slugify

from math import ceil, floor

from solaris.warbook.models import House
from solaris.warbook.techtree.models import Technology
from solaris.warbook.equipment.models import Equipment
from solaris.warbook.pilotskill.models import PilotTraitGroup, PilotRank
from solaris.campaign.models import BroadcastWeek, Campaign, createInitialPilots

def stable_icon_path(instance, filename):
    extension = filename.rsplit('.',1)[1]
    return '%s/icon.%s' % (instance.stable_slug, extension)

def stable_bg_path(instance, filename):
    extension = filename.rsplit('.',1)[1]
    return '%s/report-bg.%s' % (instance.stable_slug, extension)

class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    stable_slug = models.CharField(max_length=50, null=True)
    owner = models.OneToOneField(User, null=True)
    house = models.ForeignKey(House, null=True)
    stable_disciplines = models.ManyToManyField(PilotTraitGroup)
    campaign = models.ForeignKey(Campaign, null=True)    
    
    stable_icon = models.ImageField(upload_to=stable_icon_path, null=True, blank=True)
    stable_bg = models.ImageField(upload_to=stable_bg_path, null=True, blank=True)

    def __unicode__(self):
        return self.stable_name
    
    def get_stableweek(self, week=None):
        if week == None:
            # No week selected, so get the latest
            return self.ledger.get(next_week = None)
        elif type(week) == BroadcastWeek:
            return self.ledger.get(week = week)
        elif type(week) == int:
            return self.ledger.get(week__week_number=week)
        else:
            raise ValueError('Week parameter does not identify a week')
    
    def current_balance(self):
        try:
            ledger = self.get_stableweek()
            return ledger.closing_balance()
        except ObjectDoesNotExist:
            return 0
    
    def week_complete(self):
        return (self.remaining_tasks == None and self.current_week.next_week != None)

    def advance(self):
        """ Handles advancing the stable and all related objects to the next Broadcast Week """
        if self.current_week.next_week == None:
            return
        
        ledger = self.ledger.get(week=self.current_week)
        ledger.advance()
        
        for pilot in self.pilots.all():
            pilot.advance()        

    def save(self, *args, **kwargs):
        if self.stable_slug == None:
            self.stable_slug = slugify(self.stable_name)

        super(Stable, self).save()
        
     
class StableWeek(models.Model):
    stable = models.ForeignKey('Stable', related_name='ledger')
    week = models.ForeignKey(BroadcastWeek)
    reputation = models.IntegerField(default=0)
    reputation_set = models.BooleanField(default=False)
    opening_balance = models.IntegerField()
    supply_contracts = models.ManyToManyField('warbook.Technology')
    supply_mechs = models.ManyToManyField('warbook.MechDesign')
    custom_designs = models.ManyToManyField('warbook.MechDesign', related_name='produced_by')
    next_week = models.OneToOneField('StableWeek', on_delete=models.SET_NULL, null=True, related_name='prev_week')
    training_points = models.IntegerField(default=0)

    def has_prev_week(self):
        return hasattr(self, 'prev_week')

    def add_custom_design(self, design):
        self.custom_designs.add(design)
        self.supply_mechs.add(design)

        if self.next_week != None:
            self.next_week.add_custom_design(design)
    
    def closing_balance(self):
        if self.entries.count() > 0:
            return self.opening_balance + self.entries.all().aggregate(models.Sum('cost'))['cost__sum']
        else:
            return self.opening_balance
            
    def closing_reputation(self):
        #TODO - Process pilot ledger and update stable reputation
        return self.reputation

    def recalculate(self):
        if self.next_week != None:
            self.next_week.opening_balance = self.closing_balance()
            self.next_week.save()

    def prominence(self):
        total = 0
        for pilot in self.pilots.filter(rank__prominence_factor__gt=0):
            total += pilot.fame * pilot.rank.prominence_factor

        return total

    def can_advance(self):
        # We can advance if the next stableweek doesn't exist, but the next broadcast week does
        return (self.next_week == None and self.week.next_week != None)

    def reputation_class(self):
        if self.reputation > 0:
            return 'face'
        elif self.reputation < 0:
            return 'heel'
        else:
            return 'neutral'

    def reputation_text(self):
        if self.reputation > 0:
            return 'Face (%i)' % self.reputation
        elif self.reputation < 0:
            return 'Heel (%i)' % -self.reputation
        else:
            return 'Neutral'
    
    def advance(self):
        if self.week.next_week == None:
            return

        # Has already been done.
        if self.next_week != None:
            return
        
        try:
            # Try to get the next week along after this one, in case it already exists
            # Should rarely return anything, but this is included as a safety feature
            self.next_week = StableWeek.objects.get(stable=self.stable, week=self.week.next_week)
            self.save()
            return self.next_week
        except ObjectDoesNotExist:
            pass
        
        self.next_week = StableWeek.objects.create(
            stable = self.stable
        ,   week = self.week.next_week
        ,   reputation = self.closing_reputation()
        ,   opening_balance = self.closing_balance()
        )

        self.next_week.custom_designs.add(*self.custom_designs.all())
        self.next_week.supply_contracts.add(*self.supply_contracts.all())
        self.save()
        self.next_week.save()

        for mech in self.mechs.filter(cored=False):
            mech.advance()

        for pilot in self.pilots.filter(wounds__lt=6):
            pilot.advance()

        return self.next_week

    def add_technology(self, tech):
        self.supply_contracts.add(tech)
        if self.next_week != None:
            self.next_week.add_technology(tech)

    def remove_technology(self, tech):
        self.supply_contracts.remove(tech)
        if self.next_week != None:
            self.next_week.remove_technology(tech)
            
    def get_absolute_url(self):
        return reverse('stable_ledger', kwargs={'week': self.week.week_number})
    
    def get_overview_query_url(self):
        return reverse('stable_query_overview', kwargs={'week': self.week.week_number})
    
    def available_equipment(self):
        eq_set = Equipment.objects.none()

        for contract in self.supply_contracts.all():
            eq_set |= contract.access_to.all()

        return eq_set         
     
    def refresh_supply_mechs(self):        
        self.supply_mechs.clear()
       
        # To speed this up, auto-add all white / green tech mechs.
        # Under our rules it's pretty much impossible to lose access to these.
        self.supply_mechs.add( *self.stable.house.produced_designs.filter(tier__lte=1) ) 
       
        if self.custom_designs.count() == 0 \
        and self.supply_contracts.filter(tier__gt=1).count() == 0:
            # No yellow techs or custom designs, so nothing more to check 
            return 

        mechList = None
        if self.supply_contracts.filter(name='Omnimechs').exists():
            mechList = self.stable.house.produced_designs.filter(tier__gt=1) | self.custom_designs.all()
        else:
            mechList = self.stable.house.produced_designs.filter(is_omni=False, tier__gt=1) | self.custom_designs.filter(is_omni=False)
        
        for mech in mechList:
            if mech.required_techs.exclude(id__in=self.supply_contracts.all()).count() == 0:
                self.supply_mechs.add(mech)      

    def contender_tp(self):
        return int(floor(self.training_points / 2.0))

    def rookie_tp(self):
        return int(ceil(self.training_points / 2.0))
   
    def assigned_tp_counts(self):
        counts = {}
        for rank in PilotRank.objects.filter(receive_tp=True):
            total_tp = self.pilots.filter(rank=rank).aggregate(models.Sum('assigned_training_points'))['assigned_training_points__sum']
            if total_tp != None:
                counts[rank.rank] = total_tp
            else:
                counts[rank.rank] = 0

        counts['Total'] = sum(counts.values())

        return counts

    def contender_assigned_tp(self):
        return self.assigned_tp_counts()['Contender']

    def rookie_assigned_tp(self):
        return self.assigned_tp_counts()['Rookie']

    def total_assigned_tp(self):
        return self.assigned_tp_counts()['Total']

    def get_sigmech_pilots(self):
        owners = self.mechs.exclude(signature_of=None).values_list('signature_of')

        return self.pilots.all_living().filter(pilot__in=owners)

    def get_ownerless_sigmechs(self):
        ''' Find all signature mechs with dead owners '''
        owners = self.pilots.all_living().values_list('pilot')

        return self.mechs.exclude(signature_of=None).exclude(signature_of__in=owners)

    def __unicode__(self):
        return '%s - Week %i' % (self.stable.stable_name, self.week.week_number)

    class Meta:
        verbose_name_plural = 'Stable Weeks'
        verbose_name = 'Stable Week'
        db_table = 'stablemanager_stableweek'
        app_label = 'stablemanager'
        
        unique_together = ('stable', 'week')
    
@receiver(m2m_changed, sender=StableWeek.supply_contracts.through)
def refresh_supply_mechs(sender, instance=None, created=False, **kwargs):
    # A supply contract has been added or removed, refresh the available mechs
    instance.refresh_supply_mechs()

@receiver(post_save, sender=StableWeek)
def cascade_updates(sender, instance=None, created=False, **kwargs):
    next_week = instance.next_week
    if next_week != None:
        next_week.opening_balance = instance.closing_balance()
        
        if not next_week.reputation_set:
            next_week.reputation = instance.reputation

        next_week.save()

@receiver(post_save, sender=Stable)
def setup_initial_ledger(sender, instance=None, created=False, **kwargs):
    if created:
        stable_week = StableWeek.objects.create(
          stable=instance
        , week=BroadcastWeek.objects.get(campaign=instance.campaign, week_number=1)
        , opening_balance=instance.campaign.initial_balance
        )
        stable_week.save()

        createInitialPilots(instance)

        stable_week.supply_contracts.add(*instance.campaign.initial_contracts.all())
        stable_week.refresh_supply_mechs()
        stable_week.save()

