from django.test import TestCase

from solaris.stablemanager.tests import StableTestMixin

class PilotQuerySetTestMixin(StableTestMixin):
    expect_count = -1

    def setUp(self):
        self.stable = self.createStable()

        self.pilots = {
          'alive'          : self.add_pilot(self.stable, pilot_callsign='Alive')
        , 'wk1-dead-wound' : self.add_pilot(self.stable, pilot_callsign='Corpse')
        , 'wk1-dead-bm'    : self.add_pilot(self.stable, pilot_callsign='Burnout')
        , 'wk1-dead-both'  : self.add_pilot(self.stable, pilot_callsign='Worn')
        , 'wk1-dead-over'  : self.add_pilot(self.stable, pilot_callsign='Spatula')
        , 'wk1-removed'    : self.add_pilot(self.stable, pilot_callsign='Awol')
        , 'wk2-dead-wound' : self.add_pilot(self.stable, pilot_callsign='Autopsy')
        , 'wk2-dead-bm'    : self.add_pilot(self.stable, pilot_callsign='Fatigue')
        , 'wk2-dead-both'  : self.add_pilot(self.stable, pilot_callsign='Casualty')
        , 'wk2-dead-over'  : self.add_pilot(self.stable, pilot_callsign='Bucket')
        , 'wk2-removed'    : self.add_pilot(self.stable, pilot_callsign='Flake')
        }

        sw = self.stable.get_stableweek(1)
        sw.week.advance()
        sw.advance()

        values = {
          'dead-wound' : (6, 0, False)
        , 'dead-bm'    : (0, 6, False)
        , 'dead-both'  : (3, 3, False)
        , 'dead-over'  : (4, 4, False)
        , 'removed'    : (0, 0, True)
        }
        for week in (1,2):
            sweek = self.stable.get_stableweek(week)

            for (subkey, (wounds, blackmarks, removed)) in values.items():
                key = 'wk%i-%s' % (week, subkey)
                (pilot, pweek) = self.pilots[key]

                pweek = pilot.weeks.get(week=sweek)
                if wounds > 0:
                    pweek.set_wounds(wounds)
 
                if blackmarks > 0:
                    pweek.set_blackmarks(blackmarks)

                if removed:
                    pweek.set_removed(True)

    def get_queryset(self):
        #STUB: Test cases to implement their own function
        return None

    def do_queryset_test(self, pilot_key, message_stub):
        qs = self.get_queryset()

        (pilot, pweek) = self.pilots[pilot_key]

        result = qs.filter(pilot=pilot).exists()
        expect = self.__class__.expected[pilot_key]

        self.assertEquals(result, expect, '%s: expected: %s, found %s' % (message_stub, expect, result))

    def test_count(self):
        result = self.get_queryset().count()
        expect = self.__class__.expect_count

        self.assertEquals(result, expect, '%s: Count check yields %i rows, expected %i' % (self.__class__, result, expect)) 

    def test_alive(self):
        self.do_queryset_test('alive', 'Living Pilot')

    def test_week1_dead_wounds(self):
        self.do_queryset_test('wk1-dead-wound', 'Dead (Hidden) Pilot, Died from Wounds')

    def test_week1_dead_bm(self):
        self.do_queryset_test('wk1-dead-bm', 'Dead (Hidden) Pilot, Died from Marks`')

    def test_week1_dead_both(self):
        self.do_queryset_test('wk1-dead-both', 'Dead (Hidden) Pilot, Died from Both')

    def test_week1_dead_over(self):
        self.do_queryset_test('wk1-dead-over', 'Dead (Hidden) Pilot, Died from Overkill')
         
    def test_week2_dead_wounds(self):
        self.do_queryset_test('wk2-dead-wound', 'Dead Pilot, Died from Wounds')

    def test_week2_dead_bm(self):
        self.do_queryset_test('wk2-dead-bm', 'Dead Pilot, Died from Marks`')

    def test_week2_dead_both(self):
        self.do_queryset_test('wk2-dead-both', 'Dead Pilot, Died from Both')

    def test_week2_dead_over(self):
        self.do_queryset_test('wk2-dead-over', 'Dead Pilot, Died from Overkill')
        
class PresentQuerysetTest(PilotQuerySetTestMixin, TestCase):
    expected = {
      'alive'          : True 
    , 'wk1-dead-wound' : False 
    , 'wk1-dead-bm'    : False 
    , 'wk1-dead-both'  : False  
    , 'wk1-dead-over'  : False 
    , 'wk1-removed'    : False 
    , 'wk2-dead-wound' : True 
    , 'wk2-dead-bm'    : True 
    , 'wk2-dead-both'  : True 
    , 'wk2-dead-over'  : True 
    , 'wk2-removed'    : False 
    }
    # + 11 default starter pilots
    expect_count = 16


    def get_queryset(self):
        sw = self.stable.get_stableweek(2)
        return sw.pilots.all_present()
        
class LivingQuerysetTest(PilotQuerySetTestMixin, TestCase):
    expected = {
      'alive'          : True 
    , 'wk1-dead-wound' : False 
    , 'wk1-dead-bm'    : False 
    , 'wk1-dead-both'  : False  
    , 'wk1-dead-over'  : False 
    , 'wk1-removed'    : False 
    , 'wk2-dead-wound' : False 
    , 'wk2-dead-bm'    : False 
    , 'wk2-dead-both'  : False 
    , 'wk2-dead-over'  : False 
    , 'wk2-removed'    : False 
    }
    # + 11 default starter pilots
    expect_count = 12

    def get_queryset(self):
        sw = self.stable.get_stableweek(2)
        return sw.pilots.all_living()
        
class DeadQuerysetTest(PilotQuerySetTestMixin, TestCase):
    expected = {
      'alive'          : False
    , 'wk1-dead-wound' : False 
    , 'wk1-dead-bm'    : False 
    , 'wk1-dead-both'  : False  
    , 'wk1-dead-over'  : False 
    , 'wk1-removed'    : False 
    , 'wk2-dead-wound' : True 
    , 'wk2-dead-bm'    : True 
    , 'wk2-dead-both'  : True 
    , 'wk2-dead-over'  : True 
    , 'wk2-removed'    : False 
    }
    expect_count = 4

    def get_queryset(self):
        sw = self.stable.get_stableweek(2)
        return sw.pilots.all_dead()
