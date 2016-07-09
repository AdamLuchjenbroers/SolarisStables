from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from decimal import Decimal

from solaris.stablemanager.ledger.models import LedgerItem
from solaris.stablemanager.mechs.models import StableMechWeek, StableMech
from solaris.warbook.mech.models import MechDesign, MechDesignLocation
from solaris.warbook.equipment.models import MechEquipment, Equipment

class RepairBill(models.Model):
    stableweek = models.ForeignKey(StableMechWeek, related_name='repairs')
    mech = models.ForeignKey(MechDesign, related_name='repairs')
    complete = models.BooleanField(default=False)
    cored = models.BooleanField(default=False)
    insurance_replacement = models.ForeignKey(StableMech, blank=True, null=True) 

    class Meta:
        verbose_name = 'Repair Bill'
        db_table = 'stablemanager_repairbill'
        app_label = 'stablemanager'

    def can_be_reopened(self):
        if self.complete == False:
            return False
        elif RepairBill.objects.filter(stableweek=self.stableweek, mech=self.mech, complete=False).count() > 0:
            # Only one active bill is permitted
            return False
        else:
            return True

    def insurance_payout(self):
        if not self.cored:
            return 0
        elif self.mech.tier == 0:
            return "Replacement Mech"
        elif self.mech.tier == 1:
            return int(self.mech.credit_value * 0.5)
        elif self.mech.tier == 2:
            return int(self.mech.credit_value * 0.3)
        elif self.mech.tier == 3:
            return int(self.mech.credit_value * 0.1)
        else: 
            return 0

    def reset_bill(self):
        self.lineitems.all().delete()
        self.locations.all().delete()
        
    def set_config(self, loadout):
        self.reset_bill()
        self.mech = loadout
        self.save()
        
        return True

    def create_ledger_entry(self):
        # Check if it  exists
        if LedgerItem.objects.filter(ref_repairbill=self).count() > 0: 
            return
        
        if self.mech.is_omni:
            mech_name = '%s %s (%s)' % (self.mech.mech_name, self.mech.mech_code, self.mech.omni_loadout)
        else:
            mech_name = '%s %s' % (self.mech.mech_name, self.mech.mech_code)

        if not self.cored:
           LedgerItem.objects.create(
              description = 'Repair Bill - %s' % mech_name
           ,  cost = -self.lineitems.total_cost()
           ,  type = 'R'
           ,  tied = True
           ,  ledger = self.stableweek.stableweek
           ,  ref_repairbill = self
           )
        elif self.mech.tier > 0:
           LedgerItem.objects.create(
              description = 'Insurance Payout - %s' % mech_name
           ,  cost = self.insurance_payout()
           ,  type = 'I'
           ,  tied = True
           ,  ledger = self.stableweek.stableweek
           ,  ref_repairbill = self
           )

        self.stableweek.cored = self.cored
        self.stableweek.save()
           
    def remove_ledger_entry(self):
        LedgerItem.objects.filter(ref_repairbill=self).delete()

        self.stableweek.cored = False
        self.stableweek.save()

    def getLocation(self, location):
        try:
            mechLocation = self.mech.locations.get(location__location=location)
            (billLocation, created) = self.locations.get_or_create(location=mechLocation)
        
            return billLocation
        except MechDesignLocation.DoesNotExist:
            return None   

    def locationState(self, location):
        return self.getLocation(location).locationState()

    def destroyLocation(self, location):
        if location == 'CT':
            self.cored = True
            self.save()
            
        self.getLocation(location).destroyLocation()

    def getDamage(self, location):
        billLocation = self.getLocation(location)
        return (billLocation.structure_lost, billLocation.armour_lost)

    def setDamage(self, location, armour=None, structure=None):
        billLocation = self.getLocation(location)
        if armour != None:
            billLocation.armour_lost = max(0, min(armour, billLocation.location.armour ))

        if structure != None:
            billLocation.structure_lost = max(0, min(structure, billLocation.location.structure))

        billLocation.update_location_line()

        if location == 'CT' and billLocation.structure_lost < billLocation.location.structure:
            self.cored = False
            self.save()

        billLocation.save()
        return (billLocation.armour_lost, billLocation.structure_lost)

    def setArmourDamage(self, location, amount):
        (armour_lost, structure_lost) = self.setDamage(location, armour=amount)
        return armour_lost 

    def setStructureDamage(self, location, amount):
        (armour_lost, structure_lost) = self.setDamage(location, structure=amount) 
        return structure_lost

    def getCritical(self, location, slot):
        billLocation = self.getLocation(location)
        try:
            billCrit = billLocation.crits.get(slot=slot)
            return billCrit.critted
        except RepairBillCrit.DoesNotExist:
            # No crit entry, therefore not critted
            return False

    def setCritical(self, location, slot, critted=True):
        billLocation = self.getLocation(location)

        billLine = RepairBillLineItem.objects.line_for_item(self.mech.item_at(location,slot), self)
        if billLine == None:
            return False
 
        critted = self.setCriticalRecord(billLine, billLocation, slot, critted)
        billLine.updateCost()
        return critted

    def setCriticalRecord(self, lineitem, location, slot, critted):
        (billCrit, critCreated) = RepairBillCrit.objects.get_or_create(
            slot = slot
          , lineitem = lineitem
          , location = location
        )
       
        if lineitem.line_type == 'Q': 
            if critted and not billCrit.critted:
                lineitem.count += 1
            elif billCrit.critted and not critted:
                lineitem.count -= 1
        elif lineitem.line_type == 'M':
            if critted and not billCrit.critted:
                lineitem.count = lineitem.item.equipment.ammo_size
                lineitem.tons = 1.0
            elif billCrit.critted and not critted:
                lineitem.count = 0
                lineitem.tons = 0
                
        billCrit.critted = critted      
        lineitem.save()
        billCrit.save()
        
        return billCrit.critted
        
    def updateStructureDamage(self):
        damageTotals = self.locations.all().aggregate(models.Sum('armour_lost'), models.Sum('structure_lost'))

        armour = self.mech.loadout.get(equipment__equipment_class='S', equipment__ssw_name__startswith='Armour')
        (armourLine, created) = self.lineitems.get_or_create(item=armour, line_type='A')
        armourLine.count = damageTotals['armour_lost__sum']
        armourLine.tons = armour.tonnage(units=armourLine.count)
        armourLine.cost = armour.cost(units=armourLine.count)
        armourLine.save()

        structure = self.mech.loadout.get(equipment__equipment_class='S', equipment__ssw_name__startswith='Structure')
        (structureLine, created) = self.lineitems.get_or_create(item = structure, line_type='S')
        structureLine.count = damageTotals['structure_lost__sum']
        structureLine.cost = structure.cost(units=structureLine.count)
        structureLine.save()

    def create_ammo_lines(self):
        for ammo in self.mech.loadout.filter(equipment__equipment_class='A'):
            self.lineitems.line_for_item(ammo, self)

    def update_labour_cost(self):
        partsCost = self.lineitems.exclude(line_type='L').aggregate(models.Sum('cost'))['cost__sum']
        labourFactor = self.mech.tonnage / Decimal(100)
        
        labourCost = int(partsCost * labourFactor)
        (labourLine, created) = self.lineitems.get_or_create(line_type='L')
        labourLine.cost = labourCost

        labourLine.save()
        
            
    def get_absolute_url(self):
        return reverse('repair_bill', kwargs={'bill': self.id})

class RepairBillLineManager(models.Manager):
    use_for_related_fields = True
    
    def line_for_item(self, item, bill):
        billLine = None

        if item == None or not item.equipment.crittable:
            return None

        if item.equipment.equipment_class == 'A':
            (billLine, lineCreated) = bill.lineitems.get_or_create(
                item = item
              , line_type = 'M'
            )
            if lineCreated:
                billLine.ammo_type = billLine.item.equipment
                billLine.save()
        else:
            (billLine, lineCreated) = bill.lineitems.get_or_create(
                item = item
              , line_type = 'Q' 
            )

        return billLine
    
    def construction_lines(self):
        order_select = {
           'ordering' : "CASE WHEN line_type = 'A' THEN 1 WHEN line_type = 'S' THEN 2 WHEN line_type = 'O' THEN 3 ELSE 4 END"
        }
        lines = self.get_queryset().filter(line_type__in=('A','S','O'), count__gt=0).extra(select=order_select).order_by('ordering', 'repairbilllocation__location__location')

        return lines

    def construction_total(self):
        return self.construction_lines().aggregate(models.Sum('cost'))['cost__sum']
    
    def equipment_lines(self):
        return self.get_queryset().filter(line_type='Q', count__gt=0).order_by('item__mountings__location__location', 'item__mountings__slots')

    def equipment_total(self):
        return self.equipment_lines().aggregate(models.Sum('cost'))['cost__sum']
    
    def ammo_lines(self):
        return self.get_queryset().filter(line_type='M', count__gt=0).order_by('item__mountings__location__location', 'item__mountings__slots')

    def ammo_total(self):
        return self.ammo_lines().aggregate(models.Sum('cost'))['cost__sum']
    
    def labour_lines(self):
        return self.get_queryset().filter(line_type='L')  

    def total_cost(self): 
        return self.get_queryset().aggregate(models.Sum('cost'))['cost__sum']
    
    def ammo_bins(self):
        return self.get_queryset().filter(line_type='M').order_by('item__mountings__location__location', 'item__mountings__slots') 
    
    
class RepairBillLineItem(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="lineitems")
    item = models.ForeignKey(MechEquipment, blank=True, null=True)
    ammo_type = models.ForeignKey(Equipment, blank=True, null=True)
    count = models.IntegerField(default=0)
    tons = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cost = models.IntegerField(default=0)
    
    line_groups = (
       ('A', 'Armour'),
       ('S', 'Structure'),
       ('O', 'Location'),
       ('Q', 'Equipment'),
       ('M', 'Ammunition'),
       ('L', 'Labour Cost'),
    )     
    line_type = models.CharField(max_length=1, choices=line_groups)

    objects = RepairBillLineManager()

    class Meta:
        verbose_name = 'Repair Bill Line'
        db_table = 'stablemanager_repairbill_line'
        app_label = 'stablemanager'
        unique_together = (('line_type','bill','item'),)

    def location_string(self):
        primaryMount = self.item.primary_location()
        return '%s %s' % (primaryMount.get_location_code(), primaryMount.slots)

    def description(self):
        if self.line_type == 'M':
            primaryMount = self.item.primary_location()
            return '[%s %s] %s' % (primaryMount.get_location_code(), primaryMount.slots, self.ammo_type.name)
        elif self.line_type == 'L':
            return 'Repairs and Installation'
        elif self.line_type == 'O':
            location = self.bill.locations.get(destroyed_line=self)
            return 'Destroyed Location - %s' % location.location.location_name()
        else:
            return self.item

    def list_ammo_types(self):
        launcher = self.item.equipment.ammo_for
        if self.line_type != 'M' or launcher == None:
            return [self.ammo_type]

        return self.bill.stableweek.stableweek.available_equipment().filter(ammo_for=launcher).distinct().order_by('-basic_ammo')

    def is_critted(self):
        return (self.crits.filter(critted=True).count() > 0)
    
    def updateEquipmentCost(self):
        criticals = self.item.equipment.criticals(mech=self.bill.mech)
        baseCost  = self.item.equipment.cost(mech=self.bill.mech)

        if self.count < criticals:
            self.cost = int(baseCost * ( Decimal(self.count) / Decimal(criticals) ))
        else:
            self.cost = baseCost
        self.save()

    def updateAmmoCost(self):
        baseCost  = self.ammo_type.cost(mech=self.bill.mech)
        ammoSize  = self.ammo_type.ammo_size

        if self.count > (ammoSize / 2):
            self.cost = baseCost
            self.tons = 1.0
        else:
            self.cost = 0
            self.tons = 0.0
        self.save()
    
    def updateCost(self):
        if self.line_type == 'Q':
            self.updateEquipmentCost()
        elif self.line_type == 'M':
            self.updateAmmoCost() 

class RepairBillCrit(models.Model):
    slot = models.IntegerField()
    critted = models.BooleanField(default=False)
    location = models.ForeignKey('RepairBillLocation', related_name='crits')
    lineitem = models.ForeignKey('RepairBillLineItem', related_name='crits')

    class Meta:
        verbose_name = 'Repair Bill Crit'
        db_table = 'stablemanager_repair_line_x_loc'
        app_label = 'stablemanager'
        unique_together = (('slot','location', 'lineitem'),)

class RepairBillLocation(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="locations")
    location = models.ForeignKey(MechDesignLocation)
    armour_lost = models.IntegerField(default=0)
    structure_lost = models.IntegerField(default=0)
    destroyed_line = models.ForeignKey(RepairBillLineItem, blank=True, null=True)

    def armourState(self):
        return {
          'armour' : self.armour_lost
        , 'structure' : self.structure_lost
        }

    def locationState(self):
        locations = { self.location.location_code() : self.armourState() }
        for rear in self.location.location.front_of.all():
            rearBill = self.bill.getLocation(rear.location)
            rearBill.destroyLocation()
            locations[rear.location] = rearBill.armourState() 

        return {
          'locations' : locations 
        , 'criticals' : dict([(crit.slot, crit.critted) for crit in self.crits.all()])
        }

    def update_location_line(self):
        if not self.location.is_front():
            # Destruction of a location is managed by the front location
            return

        if self.destroyed_line == None:
            self.destroyed_line = self.bill.lineitems.create(line_type='O')

        destroyed = (self.structure_lost >= self.location.structure)

        if destroyed:
            self.destroyed_line.count = 1
            loc = self.location.location_code()
            if loc in ('RT','LT'):
                self.destroyed_line.cost = 1500 * self.bill.mech.tonnage
            elif loc in ('RL','LL','RA','LA','RRL','LRL','RFL','LFL'):
                self.destroyed_line.cost = 1000 * self.bill.mech.tonnage
            elif loc == 'HD':
                self.destroyed_line.cost = 500 * self.bill.mech.tonnage
            else:
                # We don't know how to handle this one, so just switch off the line.
                self.destroyed_line.count = 0
        else:
            self.destroyed_line.count = 0
            self.destroyed_line.cost  = 0
        self.destroyed_line.save()
        self.save()
        

    def destroyLocation(self):
        self.armour_lost = self.location.armour
        if self.location.structure != None:
            self.structure_lost = self.location.structure
        self.update_location_line()

        for item in self.location.criticals.all():
            billLine = RepairBillLineItem.objects.line_for_item(item.equipment, self.bill)
            if billLine == None:
                continue

            for slot in item.get_slots():
                self.bill.setCriticalRecord(billLine, self, slot, True)
            billLine.updateCost()
        self.save()

    class Meta:
        verbose_name = 'Repair Bill Location'
        db_table = 'stablemanager_repairbill_loc'
        app_label = 'stablemanager'
        unique_together = (('bill','location'),)

@receiver(post_save, sender=RepairBill)
def onBillUpdate(sender, instance=None, created=False, **kwargs):
    if created:
        instance.create_ammo_lines()

@receiver(post_save, sender=RepairBillLocation)
def onLocationUpdate(sender, instance=None, created=False, **kwargs):
    instance.bill.updateStructureDamage()

@receiver(post_save, sender=RepairBillLineItem)
def updateLabourCost(sender, instance=None, created=False, **kwargs):
    if instance.line_type != 'L':
       instance.bill.update_labour_cost() 
