from django.test import TestCase

from solaris.stablemanager.tests import StableTestMixin

class StableMechCreationTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.mech = self.addMech(self.stable, mech_name='Wolverine', mech_code='WVR-7D') 

    def test_stableMechWeekExists(self):
        week = self.stable.get_stableweek()
        smw = self.mech.weeks.filter(stableweek=week)
        self.assertEquals(smw.count(), 1, 'Expected one StableMechWeek record, found %i' % smw.count())

    def test_ledgerItemExists(self):
        week = self.stable.get_stableweek()
        ledger = week.entries.filter(ref_mechdesign=self.mech.purchased_as, type='P')
        self.assertEquals(ledger.count(), 1, 'Expected one StableMechWeek record, found %i' % ledger.count())

    def test_ledgerItemTied(self):
        week = self.stable.get_stableweek()
        ledger = week.entries.get(ref_mechdesign=self.mech.purchased_as, type='P')
        self.assertTrue(ledger.tied, 'Created ledger entry should be tied')

    def test_ledgerCostCorrect(self):
        week = self.stable.get_stableweek()
        ledger = week.entries.get(ref_mechdesign=self.mech.purchased_as, type='P')
        self.assertEquals(self.mech.purchased_as.credit_value, -ledger.cost
                           , 'Cost of mech incorrect, expected %i, found %i' 
                           % (self.mech.purchased_as.credit_value, -ledger.cost))
 
