from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

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

    def assertEquipment(self, location, slots, ssw_name):
        try:
            mount = self.mech.locations.get(location__location=location).criticals.get(slots=slots)
        except ObjectDoesNotExist:
            #Deliberately fail here, since apparently we couldn't find the object in these slots
            self.assertTrue(False, "Unable to find mounting in %s, slots %s" % (location, slots))

        mounted_name = mount.equipment.equipment.ssw_name
        self.assertEqual(mounted_name, ssw_name, "Object mounted in %s [%s] is %s, not %s" % (location, slots, mounted_name, ssw_name))


class WolverineTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Wolverine'
    ,   'mech_code'    : 'WVR-7D'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,5]

    def test_hands(self):
        self.assertEquipment('LA','4','Actuator - Hand')
        self.assertEquipment('RA','4','Actuator - Hand')

    def test_engine(self):
        self.assertEquipment('CT','1,2,3,8,9,10','Engine - XL Engine')

    def test_engine(self):
        self.assertEquipment('CT','4,5,6,7','Gyro - Standard Gyro')

class RavenTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Raven'
    ,   'mech_code'    : 'RVN-4L'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [6,9,0]
 
