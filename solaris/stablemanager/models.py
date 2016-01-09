from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.forms.models import model_to_dict

from solaris.warbook.models import House
from solaris.warbook.techtree.models import Technology
from solaris.warbook.equipment.models import Equipment
from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.campaign.models import BroadcastWeek, Campaign, createInitialPilots

class Stable(models.Model):
    stable_name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, null=True)
    house = models.ForeignKey(House, null=True)
    stable_disciplines = models.ManyToManyField(PilotTraitGroup)
    campaign = models.ForeignKey(Campaign, null=True)    

    def __unicode__(self):
        return self.stable_name
    
    def get_stableweek(self, week=None):
        if week == None:
            # No week selected, so get the latest
            return self.ledger.get(next_week = None)
        else:
            return self.ledger.get(week = week)
    
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
        
     
class StableWeek(models.Model):
    stable = models.ForeignKey('Stable', related_name='ledger')
    week = models.ForeignKey(BroadcastWeek)
    reputation = models.IntegerField(default=0)
    opening_balance = models.IntegerField()
    supply_contracts = models.ManyToManyField('warbook.Technology')
    supply_mechs = models.ManyToManyField('warbook.MechDesign')
    next_week = models.OneToOneField('StableWeek', null=True, related_name='prev_week')

    def has_prev_week(self):
        return hasattr(self, 'prev_week')
    
    def closing_balance(self):
        balance = self.opening_balance
        
        for item in self.entries.all():
            balance += item.get_cost()
            
        return balance

    def recalculate(self):
        try:
            prev_week = self.prev_week.get(next_week=self)
            self.opening_balance = prev_week.closing_balance()
        except StableWeek.DoesNotExist:
            pass

        if self.next_week != None:
            self.next_week.recalculate()

    def prominence(self):
        #TODO: Compute this using underlying pilots
        return 0

    def can_advance(self):
        # We can advance if the next stableweek doesn't exist, but the next week does
        return (self.next_week == None and self.week.next_week != None)
    
    def advance(self):
        if self.week.next_week == None:
            return

        # Has already been done.
        if self.next_week != None:
            return
        
        try:
            # Try to get the next week along after this one, in case it already exists
            # Should rarely return anything, but this is included as a safety feature
            self.next_week = self.objects.get(stable=self.stable, week=self.week.next_week)
            self.save()
            return self.next_week
        except ObjectDoesNotExist:
            pass
        
        self.next_week = self.objects.create(
            stable = self.stable
        ,   week = self.week.next_week
        ,   supply_contracts = self.supply_contracts
        ,   reputation = self.reputation
        ,   opening_balance = self.closing_balance()
        )
        self.save()

        for mech in self.mechs.all():
            fields = model_to_dict(mech)

            del fields['id']
            del fields['stableweek']
            self.next_week.mechs.create(**fields)    
        
        return self.next_week
            
    def get_absolute_url(self):
        return reverse('stable_ledger', kwargs={'week': self.week.week_number})
    
    def available_equipment(self):
        eq_set = Equipment.objects.none()

        for contract in self.supply_contracts.all():
            eq_set |= contract.access_to.all()

        return eq_set         
     
    def refresh_supply_mechs(self):
        equipment_list = self.available_equipment()
        
        mechList = None
        
        if self.supply_contracts.filter(name='Omnimechs').exists():
            mechList = self.stable.house.produced_designs.all()
        else:
            mechList = self.stable.house.produced_designs.filter(is_omni=False)
              
        self.supply_mechs.clear()
        
        for mech in mechList:
            if mech.can_be_produced_with(equipment_list):
                self.supply_mechs.add(mech)      

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

    
@receiver(post_save, sender=Stable)
def setup_initial_ledger(sender, instance=None, created=False, **kwargs):
    if created:
        stable_week = StableWeek.objects.create(
          stable=instance
        , week=BroadcastWeek.objects.current_week()
        , opening_balance=instance.campaign.initial_balance
        )
        stable_week.save()

        createInitialPilots(instance)

        stable_week.supply_contracts.add(*instance.campaign.initial_contracts.all())
        stable_week.refresh_supply_mechs()
        stable_week.save()

