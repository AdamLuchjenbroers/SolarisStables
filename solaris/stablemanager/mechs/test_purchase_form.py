from django.test import TestCase, Client

from solaris.warbook.mech.models import MechDesign

class PurchaseTestMixin(object):
    expect_ledger = True

    def create_stable(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')

    def test_response_success(self):
        self.assertEqual(response.status_code, 200, 'Mech purchase reported unexpected status (HTTP %s)' % response.status_code)
  
    def test_mech_added(self):
        count = self.stable.stablemech_set.filter(purchased_as=self.get_expected_mech()) 
        self.assertEqual(count, 1, 'Cannot find purchased mech in stable')

    def test_ledger_correct(self):
        sw = self.stable.get_stableweek(1)
        count = self.entries.filter(ref_mechdesign=self.get_expected_mech(), type='P') 
        if self.__class__.expect_ledger:
            self.assertNotEqual(count, 1, 'Expected 1 Ledger entry for new mech, found none.')
        else:
            self.assertNotEqual(count, 0, 'Ledger Entry not requested, should not exist.')

class PurchaseProductionMechTest(PurchaseTestMixin, TestCase):
    def setUp(self):
        self.create_stable()

        formdata = {
          'mech_source' : 'C'
        , 'mech_name' : 'Wolverine'
        , 'mech_code' : 'WVR-7D'
        , 'as_purchase' : self.__class__.expect_ledger
        }
        self.response = self.client.post('/stable/mechs/upload/purchase', formdata)

    def get_expected_mech(self):
        return MechDesign.objects.get(mech_name='Wolverine',mech_code='WVR-7D')
