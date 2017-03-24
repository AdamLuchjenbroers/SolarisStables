from django.test import TestCase

from solaris.stablemanager.tests import StableTestMixin

class MechQuerySetTestMixin(StableTestMixin):
    expect_count = -1
        
    def get_queryset(self):
        #STUB: Test cases to implement their own function
        return None

    def do_queryset_test(self, status_code, message_stub):
        qs = self.get_queryset()

        result = qs.filter(stablemech=self.mechs[status_code]).exists()
        expect = self.__class__.expected[status_code]

        self.assertEquals(result, expect, '%s: expected: %s, found %s' % (message_stub, expect, result))

    def test_count(self):
        result = self.get_queryset().count()
        expect = self.__class__.expect_count

        self.assertEquals(result, expect, '%s: Count check yields %i rows, expected %i' % (self.__class__, result, expect)) 

    def test_available_count(self):
        sw = self.stable.get_stableweek(1)
        
        result = sw.mechs.count_all_available()
        expect = self.__class__.available_count

        self.assertNotEquals(expect, result, 'count_all_available() returns incorrect count -  expected %i, got %i' % (expect, result))

class MechStatusTestMixin(MechQuerySetTestMixin):
    expected = {
      'O' : True
    , 'X' : True
    , 'R' : True
    , 'D' : True
    , 'A' : True
    , '-' : True
    }

    def setUp(self):
        self.stable = self.createStable()

        self.mechs = {
          'O' : self.addMech(self.stable, mech_name='Wolverine', mech_code='WVR-7D')
        , 'X' : self.addMech(self.stable, mech_name='Hatchetman', mech_code='HCT-3F')
        , 'R' : self.addMech(self.stable, mech_name='Dervish', mech_code='DV-8D')
        , 'D' : self.addMech(self.stable, mech_name='Raven', mech_code='RVN-4L')
        , 'A' : self.addMech(self.stable, mech_name='Griffin', mech_code='GRF-1N')
        , '-' : self.addMech(self.stable, mech_name='Quickdraw', mech_code='QKD-8X')
        }

        sw = self.stable.get_stableweek(1)

        for (status, mech) in self.mechs.items():
            mechweek = mech.weeks.get(stableweek = sw)
            mechweek.set_status(status)

    def test_operational(self):
        self.do_queryset_test('O', 'Check by status code failed')

    def test_cored(self):
        self.do_queryset_test('X', 'Check by status code failed')

    def test_removed(self):
        self.do_queryset_test('R', 'Check by status code failed')

    def test_display(self):
        self.do_queryset_test('D', 'Check by status code failed')

    def test_auction(self):
        self.do_queryset_test('A', 'Check by status code failed')

    def test_hidden(self):
        self.do_queryset_test('-', 'Check by status code failed')

         
class TestOperationalDataset(MechStatusTestMixin, TestCase):
    expected = {
      'O' : True
    , 'X' : False
    , 'R' : False
    , 'D' : False
    , 'A' : False
    , '-' : False
    }
    expect_count = 1
    available_count = 5

    def get_queryset(self):
        sw = self.stable.get_stableweek(1)
        return sw.mechs.all_operational()
         
class TestVisibleDataset(MechStatusTestMixin, TestCase):
    expected = {
      'O' : True
    , 'X' : True
    , 'R' : True
    , 'D' : True
    , 'A' : True
    , '-' : False
    }
    expect_count = 5
    available_count = 5

    def get_queryset(self):
        sw = self.stable.get_stableweek(1)
        return sw.mechs.visible()

class TestOnOrderDataset(MechQuerySetTestMixin, TestCase):
    expected = {
      0 : False
    , 1 : True
    , 2 : True
    }
    expect_count = 2
    available_count = 1

    def setUp(self):
        self.stable = self.createStable()

        self.mechs = {
          0 : self.addMech(self.stable, mech_name='Wolverine', mech_code='WVR-7D')
        , 1 : self.addMech(self.stable, mech_name='Hatchetman', mech_code='HCT-3F')
        , 2 : self.addMech(self.stable, mech_name='Dervish', mech_code='DV-8D')
        }

        sw = self.stable.get_stableweek(1)
        for (delivery, mech) in self.mechs.items():
            mechweek = mech.weeks.get(stableweek = sw)
            mechweek.delivery = delivery
            mechweek.save()

    def get_queryset(self):
        sw = self.stable.get_stableweek(1)
        return sw.mechs.on_order()

    def test_present(self):
        self.do_queryset_test(0, 'Available mech appears in on delivery list')

    def test_delivery_1wk(self):
        self.do_queryset_test(1, 'On order(1 week) mech missing from delivery list')

    def test_delivery_2wk(self):
        self.do_queryset_test(2, 'On order(1 week) mech missing from delivery list')

    def test_queryset_count(self):
        sw = self.stable.get_stableweek(1)
        
        result = sw.mechs.mechs_on_order()
        expect = self.__class__.expect_count

        self.assertNotEquals(expect, result, 'mechs_on_order() returns incorrect count -  expected %i, got %i' % (expect, result))

        
