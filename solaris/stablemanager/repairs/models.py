from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        mechLocation = self.mech.locations.get(location__location=location)
        (billLocation, created) = self.locations.get_or_create(location=mechLocation)
        
        return billLocation   

    def setDamage(self, location, armour=None, structure=None):
        billLocation = self.getLocation(location)
        if armour != None:
            billLocation.armour_lost = max(0, min(armour, billLocation.location.armour ))

        if structure != None:
            billLocation.structure_lost = max(0, min(structure, billLocation.location.structure))

        billLocation.save()

    def setArmourDamage(self, location, amount):
        self.setDamage(location, armour=amount) 

    def setStructureDamage(self, location, amount):
        self.setDamage(location, structure=amount) 

    def setCritical(self, location, slot, critted=True):
        billLocation = self.getLocation(location)
        (billLine, lineCreated) = self.lineitems.get_or_create(
            item = self.mech.item_at(location, slot)
          , line_type = 'Q' 
        )
        (billCrit, critCreated) = RepairBillCrit.objects.get_or_create(
            slot = slot
          , lineitem = billLine
          , location = billLocation
        )
        
        if critted and not billCrit.critted:
            billLine.count += 1
        elif billCrit.critted and not critted:
            billLine.count -= 1
        billCrit.critted = critted
        
        criticals = billLine.item.equipment.criticals(mech=self.mech)
        baseCost  = billLine.item.equipment.cost(mech=self.mech)
        if billLine.count < criticals:
            billLine.cost = int(baseCost * ( Decimal(billLine.count) / Decimal(criticals) ))
        else:
            billLine.cost = baseCost
        
        billLine.save()
        billCrit.save()

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


class RepairBillLineItem(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="lineitems")
    item = models.ForeignKey(MechEquipment, blank=True, null=True)
    count = models.IntegerField(default=0)
    tons = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cost = models.IntegerField(default=0)
    
    line_groups = (
       ('A', 'Armour'),
       ('S', 'Structure'),
       ('Q', 'Equipment'),
       ('M', 'Ammunition'),
       ('L', 'Labour Cost'),
    )     
    line_type = models.CharField(max_length=1, choices=line_groups)

    class Meta:
        verbose_name = 'Repair Bill Line'
        db_table = 'stablemanager_repairbill_line'
        app_label = 'stablemanager'
        unique_together = (('line_type','bill','item'),)

class RepairBillCrit(models.Model):
    slot = models.IntegerField()
    critted = models.BooleanField(default=False)
    location = models.ForeignKey('RepairBillLocation')
    lineitem = models.ForeignKey('RepairBillLineItem')

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
