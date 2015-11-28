from django.test import TestCase

from solaris.warbook.mech.models import MechDesign

class MechTestMixin(object):
    mech_ident = {
        'mech_name'    : 'MechName'
    ,   'mech_code'    : 'MN-1T'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,0]

    def setUp(self):
        self.mech = MechDesign.objects.get(**self.__class__.mech_ident)

    def mp_comparison(self, mp, expected, errorText):
        self.assertEqual(mp, expected, errorText % (mp, expected))

    def test_walkingMP(self):
        self.mp_comparison(self.mech.move_walk(), self.__class__.movement_profile[0]
                          , 'Walking MP Failed, expected %i, got %i')

    def test_runningMP(self):
        self.mp_comparison(self.mech.move_run(), self.__class__.movement_profile[1]
                          , 'Running MP Failed, expected %i, got %i')
        
    def test_jumpMP(self):
        self.mp_comparison(self.mech.move_jump(), self.__class__.movement_profile[2]
                          , 'Jumping MP Failed, expected %i, got %i')

class WolverineTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Wolverine'
    ,   'mech_code'    : 'WVR-7D'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,5]

class RavenTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Raven'
    ,   'mech_code'    : 'RVN-4L'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [6,9,0]
 
