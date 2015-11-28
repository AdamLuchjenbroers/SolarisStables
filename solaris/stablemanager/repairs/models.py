from django.db import models

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

    def updateStructureDamage(self):
        damageTotals = self.locations.all().aggregate(models.Sum(armour_lost), models.Sum(structure_lost))

        (armour, created) = self.lineitems.get_or_create(item=None, line_type='A')
        if created:
            armour.item = self.mech.loadout.get(equipment__equipment_class='S', equipment__ssw_name__startswith='Armour')
        armour.count = damageTotals['sum__armour_lost']
        armour.save()

        (structure, created) = self.lineitems.get_or_create(item=None, line_type='S')
        if created:
            structure.item = self.mech.loadout.get(equipment__equipment_class='S', equipment__ssw_name__startswith='Structure')
        structure.count = damageTotals['sum__structure_lost']
        structure.save()

class RepairBillLineItem(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="lineitems")
    item = models.ForeignKey(MechEquipment, blank=True, null=True)
    count = models.IntegerField()
    cost = models.IntegerField()
    
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

class RepairBillCrit(models.Model):
    slot = models.IntegerField()
    critted = models.BooleanField(default=True)
    location = models.ForeignKey('RepairBillLocation')
    lineitem = models.ForeignKey('RepairBillLineItem')

    class Meta:
        verbose_name = 'Repair Bill Crit'
        db_table = 'stablemanager_repair_line_x_loc'
        app_label = 'stablemanager'

class RepairBillLocation(models.Model):
    bill = models.ForeignKey(RepairBill, related_name="locations")
    location = models.ForeignKey(MechDesignLocation)
    armour_lost = models.IntegerField()
    structure_lost = models.IntegerField()

    class Meta:
        verbose_name = 'Repair Bill Location'
        db_table = 'stablemanager_repairbill_loc'
        app_label = 'stablemanager'

