from django.test import TestCase

from django.contrib.auth.models import User

from solaris.warbook.models import House
from solaris.campaign.models import Campaign 
from solaris.stablemanager.tests import StableTestMixin
from solaris.stablemanager.models import Stable, StableWeek

from .models import RepairBill

class RepairBillTestMixin(StableTestMixin):
    def setUp(self):
        self.stable = self.createStable()
        self.mech = self.addMech(self.stable, mech_name='Griffin', mech_code='GRF-1N')

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
