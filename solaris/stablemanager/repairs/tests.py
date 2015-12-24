from django.test import TestCase

from django.contrib.auth.models import User

from solaris.warbook.models import House
from solaris.campaign.models import Campaign 
from solaris.stablemanager.tests import StableTestMixin
from solaris.stablemanager.models import Stable, StableWeek

from .models import RepairBill

class RepairBillTestMixin(StableTestMixin):
    repairMech = { 'mech_name' : 'Griffin', 'mech_code' : 'GRF-1N' }

    def setUp(self):
        self.stable = self.createStable()
        self.mech = self.addMech( self.stable
                                , mech_name=self.__class__.repairMech['mech_name']
                                , mech_code=self.__class__.repairMech['mech_code']
                                )

        stableweek = self.stable.get_stableweek()

        self.bill = RepairBill.objects.create( stableweek = self.mech.get_mechweek()
                                             , mech = self.mech.purchased_as
                                             )
    def damageArmour(self, damagePattern):
        for (location, amount) in damagePattern:
            self.bill.setArmourDamage(location, amount)

    def damageStructure(self, damagePattern):
        for (location, amount) in damagePattern:
            self.bill.setStructureDamage(location, amount)

class DamageResultTests(RepairBillTestMixin, TestCase):
    def test_armourDamage(self):
        damage_done = self.bill.setArmourDamage('CT', 15)
        self.assertEqual(damage_done, 15, 'Expecting damage done to equal 15, got %i' % damage_done)
        
    def test_armourDamageMax(self):
        damage_done = self.bill.setArmourDamage('CT', 25)
        self.assertEqual(damage_done, 20, 'Expecting damage done to equal 20, got %i' % damage_done)
        
    def test_structureDamage(self):
        damage_done = self.bill.setStructureDamage('CT', 15)
        self.assertEqual(damage_done, 15, 'Expecting damage done to equal 15, got %i' % damage_done)
        
    def test_structureDamageMax(self):
        damage_done = self.bill.setStructureDamage('CT', 25)
        self.assertEqual(damage_done, 18, 'Expecting damage done to equal 18, got %i' % damage_done)

    def test_criticalItem(self):
        critted = self.bill.setCritical('RT',4)
        self.assertTrue(critted, 'Critical failed to register for Right Torso 4 (LRM-10)')

    def test_criticalItemClear(self):
        critted = self.bill.setCritical('RT',4, critted=False)
        self.assertFalse(critted, 'Critical failed to clear for Right Torso 4 (LRM-10)')

    def test_criticalItemEmpty(self):
        critted = self.bill.setCritical('RT',8, critted=False)
        self.assertFalse(critted, 'Critical incorrectly registered for empty slot (Right Torso 8)')        
        
class BasicRepairBillTests(RepairBillTestMixin, TestCase):
    def test_billIncomplete(self):
        # A freshly created bill should start marked incomplete
        self.assertFalse(self.bill.complete, 'Repair Bill should not be marked complete when created')

class ArmourRepairTests(RepairBillTestMixin, TestCase):
    def test_armourLineItem(self):
        self.damageArmour([('RT', 12),])

        # Check the armour line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.count, 12, 'Armour Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 20))

    def test_armourLineItemMax(self):
        self.damageArmour([('RT', 30),])

        # Check the armour line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.count, 20, 'Armour Line-item should be maximum (%i), got %i' % (20, lineitem.count))

    def test_armourNoDuplicates(self):
        self.damageArmour([('RT', 30), ('LT', 15), ('RL', 20)])

        records = self.bill.lineitems.filter(line_type='A').count()
        self.assertEquals(records, 1, 'Duplicate Armour Line-items created')

    def test_armourSum(self):
        self.damageArmour([('RT', 20), ('CT', 14), ('LT', 10), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.count, 56, 'Summed armour Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 65))

    def test_armourTons(self):
        self.damageArmour([('RT', 20), ('CT', 14), ('LT', 10), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.tons, 3.5, 'Summed armour Line-item has incorrect tonnage, got %.1f, expected %.1f' % (lineitem.tons, 3.5))

    def test_armourCost(self):
        self.damageArmour([('RT', 20), ('CT', 14), ('LT', 10), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.cost, 35000.00, 'Summed armour Line-item has incorrect cost, got %.1f, expected %.1f' % (lineitem.cost, 35000.00))

class StructureRepairTests(RepairBillTestMixin, TestCase):
    def test_structureLineItem(self):
        self.damageStructure([('RT', 12),])

        # Check the structure line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.count, 12, 'Structure Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 12))

    def test_structureLineItemMax(self):
        self.damageStructure([('RT', 20),])

        # Check the structure line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.count, 13, 'Structure Line-item should be maximum (%i), got %i' % (13, lineitem.count))

    def test_structureNoDuplicates(self):
        self.damageStructure([('RT', 12), ('LT', 8), ('RL', 4)])

        records = self.bill.lineitems.filter(line_type='S').count()
        self.assertEquals(records, 1, 'Duplicate Structure Line-items created')

    def test_structureSum(self):
        self.damageStructure([('RT', 12), ('LT', 8), ('RL', 4)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.count, 24, 'Summed structure Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 24))

    def test_structureTons(self):
        self.damageStructure([('RT', 30), ('CT', 14), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.tons, None, 'Summed structure Line-item has a tonnage, this column should be blank')

    def test_structureCost(self):
        self.damageStructure([('RT', 12), ('LT', 8), ('RL', 4)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.cost, 15000.00, 'Summed structure Line-item has incorrect cost, got %.1f, expected %.1f' % (lineitem.cost, 35000.00))

class GyroRepairTests(RepairBillTestMixin, TestCase):
    def setUp(self):
        super(GyroRepairTests, self).setUp()
       
        # Gyro
        self.bill.setCritical('CT',5)
        
    def test_expectedCrits(self):
        count = self.bill.lineitems.filter(line_type='Q', item__equipment__ssw_name = 'Gyro - Standard Gyro').count()
        self.assertEqual(count, 1, 'Expected a single line for the damaged gyro, found %i' % count)
    
    def test_gyroCost(self):
        line = self.bill.lineitems.get(line_type='Q', item__equipment__ssw_name = 'Gyro - Standard Gyro')
        # 275 Engine = 3 Ton gyro, (3 x 300000/4) = 225000 per critical slot
        self.assertEqual(line.cost, 225000, 'Incorrect gyro cost, expected FIXME, found %i' % line.cost)

class EquipmentRepairTests(RepairBillTestMixin, TestCase):
    def setUp(self):
        super(EquipmentRepairTests, self).setUp()
       
        # 1 Heatsink 
        self.bill.setCritical('CT',11)

        # 2 Jump jets
        self.bill.setCritical('CT',12)
        self.bill.setCritical('RT',1)

        # 2 Crits to the PPC
        self.bill.setCritical('RA',5)
        self.bill.setCritical('RA',6)

    def test_heatsinkLineItem(self):
        count = self.bill.lineitems.filter(line_type='Q', item__equipment__ssw_name = 'Heatsink - Single Heat Sink').count()
        self.assertEquals(count, 1, 'Expected line items to contain one Heat Sink, %i found' % count)

    def test_heatsinkCost(self):
        heatsink = self.bill.lineitems.get(line_type='Q', item__equipment__ssw_name = 'Heatsink - Single Heat Sink')
        self.assertEquals(heatsink.cost, 2000, 'Expected cost for heatsink to be 2000, got %i' % heatsink.cost)

    def test_jumpjetLineItem(self):
        count = self.bill.lineitems.filter(line_type='Q', item__equipment__ssw_name = 'Jumpjet - Standard Jump Jet').count()
        self.assertEquals(count, 2, 'Expected line items to contain two Jump Jets, %i found' % count)

    def test_jumpjetCost(self):
        jet = self.bill.lineitems.filter(line_type='Q', item__equipment__ssw_name = 'Jumpjet - Standard Jump Jet')[0]
        self.assertEquals(jet.cost, 55000, 'Expected cost to repair 1 jumpjet of 5 is 55000, %i found' % jet.cost)

    def test_ppcLineItem(self):
        count = self.bill.lineitems.filter(line_type='Q', item__equipment__ssw_name = 'Equipment - (IS) PPC').count()
        self.assertEquals(count, 1, 'Expected line items to contain one PPC, %i found' % count)

    def test_ppcCost(self):
        ppc = self.bill.lineitems.get(line_type='Q', item__equipment__ssw_name = 'Equipment - (IS) PPC')
        self.assertEquals(ppc.cost, 133333, 'Expected cost for PPC (2 crits) to be 133333, got %i' % ppc.cost)

class LabourCostTests(RepairBillTestMixin, TestCase):
    def test_singleItemRecord(self):
        # JumpJet  
        self.bill.setCritical('CT',12) # Jump Jet (55000 cbills)
        count = self.bill.lineitems.filter(line_type='L').count()
        self.assertEquals(count, 1, 'Only a single labour cost entry should exist, found %i' % count)

    def test_singleItemCost(self):
        self.bill.setCritical('CT',12) # Jump Jet (55000 cbills)

        lineitem = self.bill.lineitems.get(line_type='L')
        # Cost should be 55000 X 0.55 (for 55 ton mech) = 30250
        self.assertEquals(lineitem.cost, 30250, 'Labour cost to repair a single jumpjet should be 30250, got %i' % lineitem.cost)

    def test_multipleItemRecord(self):
        self.bill.setCritical('CT',12) # Jump Jet (55000 cbills)
        self.bill.setCritical('RT',3) # First slot of an LRM-10 (50000 cbills)

        count = self.bill.lineitems.filter(line_type='L').count()
        self.assertEquals(count, 1, 'Only a single labour cost entry should exist, found %i' % count)

    def test_multipleItemCost(self):
        self.bill.setCritical('CT',12) # Jump Jet (55000 cbills)
        self.bill.setCritical('RT',3) # First slot of an LRM-10 (50000 cbills)

        lineitem = self.bill.lineitems.get(line_type='L')
        # Cost should be 105000 X 0.55 (for 55 ton mech) = 57750
        self.assertEquals(lineitem.cost, 57750, 'Labour cost to repair a jumpjet and LRM should be 57750, got %i' % lineitem.cost)

class DestroyedAmmoTests(RepairBillTestMixin, TestCase):
    def setUp(self):
        super(DestroyedAmmoTests, self).setUp()
        self.bill.setCritical('RT',5) # LRM-10 Ammo bin
        self.lineitem = self.bill.lineitems.get(line_type='M', item__equipment__ssw_name = 'Ammo - (IS) @ LRM-10')

    def test_checkAmmoCount(self):
        self.assertEqual(self.lineitem.count, 12, 'Ammo Count for a destroyed LRM-10 ammo bin should be 12, got %i' % self.lineitem.count) 

    def test_checkAmmoTons(self):
        self.assertEqual(self.lineitem.tons, 1.0, 'Used tonnage a destroyed LRM-10 ammo bin should be 1.0, got %.1f' % self.lineitem.tons) 

class NonCrittableItemTests(RepairBillTestMixin, TestCase):
    repairMech = { 'mech_name' : 'Wolverine', 'mech_code' : 'WVR-7D' }

    def test_singleCrit(self):
        self.bill.setCritical('LA',5)
        count = self.bill.lineitems.filter(line_type='Q').count()
        self.assertEqual(count, 0, 'Should be no line items after a single crit to ferro-fibrous, found %i' % count)

    def test_destroyedLocation(self):
        self.bill.destroyLocation('LA')
        count = self.bill.lineitems.filter(line_type='Q').count()
        self.assertEqual(count, 4, 'Should be four destroyed items in left arm, found %i' % count)

class DestroyedLocationTests(RepairBillTestMixin, TestCase):
    def setUp(self):
        super(DestroyedLocationTests, self).setUp()
        self.bill.destroyLocation('RT')

    def test_armour(self):
        location = self.bill.getLocation('RT')
        self.assertEquals(location.armour_lost, 20, 'Expected all right torso armour (20) to be lost, got %i' % location.armour_lost)

    def test_structure(self):
        location = self.bill.getLocation('RT')
        self.assertEquals(location.structure_lost, 13, 'Expected all right torso structure (13) to be lost, got %i' % location.structure_lost)
    
    def test_jumpjetsDestroyed(self):
        count = self.bill.lineitems.filter(line_type='Q', count=1, item__equipment__ssw_name = 'Jumpjet - Standard Jump Jet').count()
        self.assertEquals(count, 2, 'Expected 2 JumpJets to be destroyed, found %i' % count)   
    
    def test_lrmDestroyed(self):
        count = self.bill.lineitems.filter(line_type='Q', count=2, item__equipment__ssw_name = 'Equipment - (IS) LRM-10').count()
        self.assertEquals(count, 1, 'Expected 1 LRM-10 to be destroyed, found %i' % count)   
    
    def test_lrmAmmoDestroyed(self):
        count = self.bill.lineitems.filter(line_type='A', item__equipment__ssw_name = 'Ammo - (IS) @ LRM-10').count()
        self.assertEquals(count, 2, 'Expected 2 LRM-10 ammo bins to be destroyed, found %i' % count)  

    def test_lrmAmmoFull(self): 
        lineitem = self.bill.lineitems.filter(line_type='A', item__equipment__ssw_name = 'Ammo - (IS) @ LRM-10')[0]
        ammosize = lineitem.item.equipment.ammo_size
        self.assertEquals(lineitem.count, ammosize, 'Expected full ammo count (%i) to be expended, found %i' % (ammosize, lineitem.count))

    def test_lrmAmmoFullTon(self): 
        lineitem = self.bill.lineitems.filter(line_type='A', item__equipment__ssw_name = 'Ammo - (IS) @ LRM-10')[0]
        self.assertEquals(lineitem.tons, 1.0, 'Destroyed ammo bin counts as full expended ton, got %.1f' % lineitem.tons)
