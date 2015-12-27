from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from decimal import Decimal

from solaris.stablemanager.mechs.models import StableMechWeek
from solaris.warbook.mech.models import MechDesign, MechDesignLocation
from solaris.warbook.equipment.models import MechEquipment

class RepairBill(models.Model):
    stableweek = models.ForeignKey(StableMechWeek, related_name='repairs')
    mech = models.ForeignKey(MechDesign)
    complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Repair Bill'
        db_table = 'stablemanager_repairbill'
        app_label = 'stablemanager'

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
        elif lineitem.line_type == 'A':
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
              , count = item.equipment.ammo_size
              , tons = Decimal(1.0) 
            )
        else:
            (billLine, lineCreated) = bill.lineitems.get_or_create(
                item = item
              , line_type = 'Q' 
            )

        return billLine
    
    def construction_lines(self):
        return self.get_queryset().filter(line_type__in=('A','S'), count__gt=0)    
    
    def equipment_lines(self):
        return self.get_queryset().filter(line_type='Q', count__gt=0).order_by('-cost')    
    
    
class RepairBillLineItem(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="lineitems")
    item = models.ForeignKey(MechEquipment, blank=True, null=True)
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
    
    def updateEquipmentCost(self):
        criticals = self.item.equipment.criticals(mech=self.bill.mech)
        baseCost  = self.item.equipment.cost(mech=self.bill.mech)

        if self.count < criticals:
            self.cost = int(baseCost * ( Decimal(self.count) / Decimal(criticals) ))
        else:
            self.cost = baseCost
        self.save()

    def updateAmmoCost(self):
        baseCost  = self.item.equipment.cost(mech=self.bill.mech)
        ammoSize  = self.item.equipment.ammo_size

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
        elif self.line_type == 'A':
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

    def locationState(self):
        return {
          'armour' : self.armour_lost
        , 'structure' : self.structure_lost
        , 'criticals' : dict([(crit.slot, crit.critted) for crit in self.crits.all()])
        }

    def destroyLocation(self):
        self.armour_lost = self.location.armour
        self.structure_lost = self.location.structure

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


@receiver(post_save, sender=RepairBillLocation)
def onLocationUpdate(sender, instance=None, created=False, **kwargs):
    instance.bill.updateStructureDamage()

@receiver(post_save, sender=RepairBillLineItem)
def updateLabourCost(sender, instance=None, created=False, **kwargs):
    if instance.line_type != 'L':
       instance.bill.update_labour_cost() 
