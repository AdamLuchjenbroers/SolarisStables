from django.db import models
from django.core.urlresolvers import reverse

from solaris.stablemanager.models import Stable, StableWeek
from solaris.stablemanager.ledger.models import LedgerItem
from solaris.warbook.mech.refit import refit_cost

class StableMechManager(models.Manager):
    def create_mech(self, stable=None, purchased_as=None, purchased_on=None, create_ledger=True, delivery=0):
        
        if purchased_as.is_omni and purchased_as.omni_basechassis != None:            
            try:
                config_for = StableMechWeek.objects.get(stableweek=purchased_on, current_design=purchased_as.omni_basechassis)
                stablemech = config_for.stablemech
                add_config = True 
            except StableMechWeek.DoesNotExist:
                stablemech = StableMech.objects.create(stable=stable, purchased_as=purchased_as.omni_basechassis)
                
                config_for = StableMechWeek.objects.create(
                  stableweek = purchased_on
                , stablemech = stablemech
                , current_design = purchased_as.omni_basechassis
                , delivery = delivery
                )
                add_config = False

        else:             
            stablemech = StableMech.objects.create(stable=stable, purchased_as=purchased_as)
            config_for = None
            add_config = False
            
        stablemechweek = StableMechWeek.objects.create(
          stableweek = purchased_on
        , stablemech = stablemech
        , current_design = purchased_as
        , delivery = delivery
        , config_for = config_for
        )
 
        if config_for == None or add_config:
            adv_smw = stablemechweek
        else:
            adv_smw = config_for

        while adv_smw.can_advance():
            if add_config:   
                adv_smw = adv_smw.advance_config()
            else:
                adv_smw = adv_smw.advance()
        
        if create_ledger:
            if add_config:
                description = 'New Loadout - %s' % purchased_as.__unicode__()
                cost = -refit_cost(purchased_as.omni_basechassis, purchased_as)
            else:
                description = 'Purchase - %s' % purchased_as.__unicode__()
                cost = -purchased_as.credit_value
                
            self.ledgeritem = LedgerItem.objects.create (
              ledger = purchased_on
            , description = description
            , cost = cost
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
 
    def get_mechweek(self, week=None, loadout='Base'):
        if week == None or type(week) == solaris.campaign.models.BroadcastWeek:
            stableweek = self.stable.get_stableweek(week=week)
        else:
            stableweek = week
        
        if self.purchased_as.is_omni:
            return self.weeks.get(stableweek=stableweek, current_design__omni_loadout=loadout)
        else:
            return self.weeks.get(stableweek = stableweek)

    class Meta:
        verbose_name_plural = 'Mechs'
        verbose_name = 'Mech'
        db_table = 'stablemanager_mech'
        app_label = 'stablemanager'

class StableMechWeekManager(models.Manager):
    use_for_related_fields = True

    def count_all_available(self):
        return self.exclude(delivery__gt=0, config_for=None, mech_status='-').count()

    def count_nonsignature(self):
        return self.visible().filter(signature_of=None, config_for=None, delivery=0).count()

    def has_signature(self):
        return self.visible().exclude(signature_of=None).count() > 0

    def non_signature(self):
        return self.visible().filter(signature_of=None, config_for=None, delivery=0).order_by('current_design__tonnage', 'current_design__mech_name')

    def mechs_on_order(self): 
        return self.visible().filter(delivery__gt=0).count >= 0

    def on_order(self):
        return self.visible().filter(delivery__gt=0, config_for=None).order_by('delivery', 'current_design__tonnage', 'current_design__mech_name')

    def production(self):
        return self.visible().filter(current_design__production_type__in=('P','H'))

    def custom(self):
        return self.visible().filter(current_design__production_type__in=('C'))

    def all_operational(self):
        return self.filter(mech_status__in=StableMechWeek.active_states)

    def visible(self):
        return self.exclude(mech_status='-')

class StableMechWeek(models.Model):
    stableweek = models.ForeignKey(StableWeek, related_name='mechs', blank=True, null=True)
    stablemech = models.ForeignKey(StableMech, related_name='weeks')
    current_design = models.ForeignKey('warbook.MechDesign')
    signature_of = models.ForeignKey('Pilot', related_name='signature_mechs', blank=True, null=True)
    next_week = models.OneToOneField('StableMechWeek', on_delete=models.SET_NULL, related_name='prev_week', blank=True, null=True)
    delivery = models.IntegerField(default=0)    
    config_for = models.ForeignKey('stablemanager.StableMechWeek', related_name='loadouts', blank=True, null=True)

    mech_states = (
        ('O', 'Fully Operational')
    ,   ('X', 'Cored')
    ,   ('D', 'On Display (Honours)')
    ,   ('R', 'To Be Removed')
    ,   ('A', 'Marked For Auction')
    ,   ('-', 'Removed (Hidden)')
    )
    mech_status = models.CharField(max_length=1, choices=mech_states, default='O', blank=False, null=False)

    active_states = ('O',)
    inactive_states = ('X', 'D', 'R', 'A', '-')

    objects = StableMechWeekManager()
    
    class Meta:
        db_table = 'stablemanager_mechweek'
        app_label = 'stablemanager'

    def active_repair_bill(self):
        from solaris.stablemanager.repairs.models import RepairBill
        try:
            return self.repairs.get(mech=self.current_design, stableweek=self, complete=False)
        except RepairBill.DoesNotExist:
            return None

    def is_display_mech(self):
        if hasattr(self.stableweek, 'honoured'):
            return self.stableweek.honoured.filter(display_mech = self.stablemech).exists()
        else:
            return False

    def set_status(self, new_status, write_locked=False):
        if self.is_locked() and not write_locked:
            #Record is locked, do not perform update
            return self.mech_status

        if self.next_week != None:
            if new_status in StableMechWeek.inactive_states:
                self.next_week.set_status('-')
            elif self.mech_status in StableMechWeek.inactive_states \
            and new_status in StableMechWeek.active_states:
                self.next_week.set_status(new_status)

        self.mech_status = new_status
        self.save()

        return self.mech_status

    def set_removed(self, value):
        if value == True and (self.next_week == None and not hasattr(self, 'prev_week')):
            self.delete()

            return True
        
        if value == True:
            self.set_status('R')
            return (self.mech_status == 'R')
        else:
            self.set_status('O')
            return (self.mech_status == 'O')

    def set_cored(self, value):
        self.set_status('X')
        return (self.mech_status == 'X')

    def core_mech(self, value):
        from solaris.stablemanager.repairs.models import RepairBill

        if value == True:
            self.removed = True

            bill = self.active_repair_bill()
            if bill == None:
                bill = RepairBill.objects.create(mech = self.current_design, stableweek=self)

            bill.cored = True
            bill.complete = True
            bill.save()
            bill.create_ledger_entry()

            self.set_status('X')

        if value == False:
            self.set_status('O')
            for bill in self.repairs.filter(cored=True):
                bill.remove_ledger_entry()
                bill.delete() 

        self.save()

        if self.next_week != None:
            self.next_week.set_cored(value)

    def completed_bill_count(self):
        return self.repairs.filter(complete=True).count()

    def refit_options(self):
        return self.stableweek.supply_mechs.exclude(id=self.current_design.id).filter(mech_name=self.current_design.mech_name, is_omni=False)

    def refit_production_options(self):
        return self.refit_options().filter(production_type__in=('P','H'))
 
    def refit_custom_options(self):
        return self.refit_options().exclude(production_type__in=('P','H'))
    
    def loadout_options(self):
        return self.stableweek.supply_mechs.exclude(id__in=self.loadouts.all().values('current_design__id')).filter(omni_basechassis=self.current_design)

    def loadout_production_options(self):
        return self.loadout_options().filter(production_type__in=('P','H'))
 
    def loadout_custom_options(self):
        return self.loadout_options().exclude(production_type__in=('P','H'))

    def is_visible(self):
        return (self.mech_status != '-')

    def is_locked(self):
        # Is this mech already linked to an auction / display
        if self.mech_status in ('D', 'A'):
            return True

        if self.next_week == None:
            return False

        # Is there already a repairbill against next week?
        if self.next_week.repairs.count() > 0:
            return True

        # Do any ledger items refer to next week?
        if LedgerItem.objects.filter(ref_stablemech_week=self.next_week).count() > 0:
            return True

        # Check if the next week is locked too
        return self.next_week.is_locked()

    def can_advance(self):
        return (self.stableweek.next_week != None) and self.mech_status not in StableMechWeek.inactive_states

    def advance(self):
        if self.stableweek.next_week == None:
            return None

        if self.next_week != None:
            return self.next_week

        if self.mech_status in StableMechWeek.inactive_states:
            return None
        
        if self.config_for != None:
            # Should be advanced by advancing it's base chassis.
            return None

        self.next_week = StableMechWeek.objects.create(
           stableweek = self.stableweek.next_week
        ,  stablemech = self.stablemech
        ,  current_design = self.current_design
        ,  signature_of = self.signature_of
        ,  mech_status = self.mech_status
        ,  delivery = max(0, self.delivery - 1)
        )
        
        for config in self.loadouts.filter(mech_status__in=StableMechWeek.active_states):
            config.advance_config()
        
        self.save()
        return self.next_week

    def advance_config(self):
        if self.config_for == None:
            # Not a config
            return None

        if self.next_week != None:
            #Already advanced to next week, just return the value.
            return self.next_week

        if self.config_for.next_week == None or self.stableweek.next_week == None:
            # No next week to advance to
            return None

        if self.mech_status in StableMechWeek.inactive_states:
            return None
        
        self.next_week = StableMechWeek.objects.create(
           stableweek = self.stableweek.next_week
        ,  stablemech = self.stablemech
        ,  current_design = self.current_design
        ,  signature_of = self.config_for.signature_of
        ,  mech_status = self.mech_status
        ,  config_for = self.config_for.next_week
        )
        self.save()
        
        return self.next_week

    def cascade_advance(self):
        if self.removed:
            return
        elif self.next_week == None:
            nextweek = self.advance()
        
        if nextweek != None:
            nextweek.cascade_advance()

    def refit_to(self, newdesign, add_ledger=False, failed_by=0):
        olddesign = self.current_design
        self.current_design = newdesign
        self.save()

        if add_ledger:
            cost = refit_cost(olddesign, newdesign)
            if failed_by > 0:
                cost += int (newdesign.credit_value * (failed_by / 10.0))

            self.ledgeritem = LedgerItem.objects.create (
              ledger = self.stableweek
            , description = 'Refit - Upgrade %s %s to %s' % (olddesign.mech_name, olddesign.mech_code, newdesign.mech_code)
            , cost = -cost
            , type = 'P'
            , tied = True
            , ref_mechdesign = newdesign
            , ref_stablemech = self.stablemech
            , ref_stablemech_week = self
            )

        if self.next_week != None:
            self.next_week.refit_to(newdesign, add_ledger=False)

    def owner_status(self):
        if self.signature_of == None:
            return None
        
        pilotweek = self.signature_of.weeks.get(week=self.stableweek)
        return pilotweek.status

    def refit_url(self):
        return reverse('refit_mech', kwargs={'smw_id' : self.id})

    def remove_url(self):
        return reverse('remove_mech', kwargs={'smw_id' : self.id})

    def edit_url(self):
        return reverse('edit_mech', kwargs={'smw_id' : self.id})

    def loadout_url(self):
        return reverse('loadout_mech', kwargs={'smw_id' : self.id})
    
    def repair_bill_url(self):
        bill = self.active_repair_bill()
        if bill != None:
            return bill.get_absolute_url()
        else:
            return reverse('repair_bill_new', kwargs={'stablemech' : self.id})
