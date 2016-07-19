from django.test import TestCase, Client

from solaris.warbook.mech.models import MechDesign
from solaris.stablemanager.tests import StableTestMixin

class PurchaseTestMixin(StableTestMixin):
    expect_ledger = True

    def createClient(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')

    def test_response_success(self):
        self.assertEqual( self.response.status_code, 200, 'Mech purchase reported unexpected status (HTTP %s)\n%s' 
                        % (self.response.status_code,self.response.content))
  
    def test_mech_added_stablemech(self):
        mech = self.get_expected_mech()
        if mech.is_omni and mech.omni_basechassis != None:
            mech = mech.omni_basechassis
 
        count = self.stable.stablemech_set.filter(purchased_as=mech).count()
        sm_list = ''
        for sm in self.stable.stablemech_set.all():
            sm_list += '\t* %s\n' % sm.purchased_as
 
        self.assertEqual(count, 1, 'Cannot find purchased StableMech in stable, %d matches. Available mechs are:\n%s' % (count,sm_list))
  
    def test_mech_added_stablemechweek(self):
        sw = self.stable.get_stableweek(1)
        expect = self.get_expected_mech()

        count = sw.mechs.filter(current_design=expect).count()
        smw_list = ''
        for smw in sw.mechs.all():
            smw_list += '\t* %s\n' % smw.current_design

        self.assertEqual(count, 1, 'Cannot find purchased StableMechWeek (%s) in stable, found:\n%s' % (expect, smw_list))

    def test_ledger_correct(self):
        sw = self.stable.get_stableweek(1)
        count = sw.entries.filter(ref_mechdesign=self.get_expected_mech(), type='P').count() 
        if self.__class__.expect_ledger:
            self.assertEqual(count, 1, 'Expected 1 Ledger entry for new mech, found %d.' % count)
        else:
            self.assertEqual(count, 0, 'Ledger Entry not requested, found %d.' % count)

class PurchaseProductionMechTest(PurchaseTestMixin, TestCase):
    def setUp(self):
        self.createClient()

        formdata = {
          'mech_source' : 'C'
        , 'mech_name' : 'Wolverine'
        , 'mech_code' : 'WVR-7D'
        , 'omni_loadout' : 'Base'
        , 'as_purchase' : str(self.__class__.expect_ledger).lower()
        , 'delivery'  : 0
        }
        self.response = self.client.post('/stable/mechs/1/purchase', formdata)

    def get_expected_mech(self):
        return MechDesign.objects.get(mech_name='Wolverine',mech_code='WVR-7D')

class PurchaseProductionMechTestNoLedger(PurchaseProductionMechTest):
    expect_ledger = False

class PurchaseProductionOmniMechTest(PurchaseTestMixin, TestCase):
    def setUp(self):
        self.createClient()

        formdata = {
          'mech_source' : 'C'
        , 'mech_name' : 'Owens'
        , 'mech_code' : 'OW-1'
        , 'omni_loadout' : 'C'
        , 'as_purchase' : self.__class__.expect_ledger
        , 'delivery'  : 0
        }
        self.response = self.client.post('/stable/mechs/1/purchase', formdata)

    def get_expected_mech(self):
        return MechDesign.objects.get(mech_name='Owens', mech_code='OW-1', omni_loadout='C')

class PurchaseProductionOmniMechTestNoLedger(PurchaseProductionOmniMechTest):
    expect_ledger = False
