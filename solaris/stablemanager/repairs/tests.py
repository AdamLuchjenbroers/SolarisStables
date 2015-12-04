from django.test import TestCase

from django.contrib.auth.models import User

from solaris.warbook.models import House
from solaris.campaign.models import Campaign 
from solaris.stablemanager.tests import StableTestMixin
from solaris.stablemanager.models import Stable, StableWeek

from .models import RepairBill

class RepairBillTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.mech = self.addMech(self.stable, mech_name='Griffin', mech_code='GRF-1N')

        stableweek = self.stable.get_stableweek()

        self.bill = RepairBill.objects.create( stableweek = self.mech.get_mechweek()
                                             , mech = self.mech.purchased_as
                                             )
    def damageArmour(self, damagePattern):
        for (locCode, amount) in damagePattern:
            locItem = self.bill.getLocation(locCode)
            locItem.armour_lost = amount
            locItem.save()

    def damageStructure(self, damagePattern):
        for (locCode, amount) in damagePattern:
            locItem = self.bill.getLocation(locCode)
            locItem.structure_lost = amount
            locItem.save()

    def test_billIncomplete(self):
        # A freshly created bill should start marked incomplete
        self.assertFalse(self.bill.complete, 'Repair Bill should not be marked complete when created')

    def test_armourLineItem(self):
        self.damageArmour([('RT', 20),])

        # Check the armour line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.count, 20, 'Armour Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 20))

    def test_armourNoDuplicates(self):
        self.damageArmour([('RT', 30), ('LT', 15), ('RL', 20)])

        records = self.bill.lineitems.filter(line_type='A').count()
        self.assertEquals(records, 1, 'Duplicate Armour Line-items created')

    def test_armourSum(self):
        self.damageArmour([('RT', 30), ('LT', 15), ('RL', 20)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.count, 65, 'Summed armour Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 65))

    def test_armourTons(self):
        self.damageArmour([('RT', 30), ('CT', 14), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.tons, 3.5, 'Summed armour Line-item has incorrect tonnage, got %.1f, expected %.1f' % (lineitem.tons, 3.5))

    def test_armourCost(self):
        self.damageArmour([('RT', 30), ('CT', 14), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='A')
        self.assertEquals(lineitem.cost, 35000.00, 'Summed armour Line-item has incorrect cost, got %.1f, expected %.1f' % (lineitem.cost, 35000.00))

    def test_structureLineItem(self):
        self.damageStructure([('RT', 20),])

        # Check the structure line-item was created correctly
        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.count, 20, 'Structure Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 20))

    def test_structureNoDuplicates(self):
        self.damageStructure([('RT', 30), ('LT', 15), ('RL', 20)])

        records = self.bill.lineitems.filter(line_type='S').count()
        self.assertEquals(records, 1, 'Duplicate Structure Line-items created')

    def test_structureSum(self):
        self.damageStructure([('RT', 30), ('LT', 15), ('RL', 20)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.count, 65, 'Summed structure Line-item has incorrect count, got %i, expected %i' % (lineitem.count, 65))

    def test_structureTons(self):
        self.damageStructure([('RT', 30), ('CT', 14), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.tons, None, 'Summed structure Line-item has a tonnage, this column should be blank')

    def test_structureCost(self):
        self.damageStructure([('RT', 30), ('CT', 14), ('RA', 12)])

        lineitem = self.bill.lineitems.get(line_type='S')
        self.assertEquals(lineitem.cost, 35000.00, 'Summed structure Line-item has incorrect cost, got %.1f, expected %.1f' % (lineitem.cost, 35000.00))

