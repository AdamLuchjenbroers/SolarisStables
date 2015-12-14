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
    directfire_tonnage = None
    check_fields = {
        'production_year'  : 3050
    ,   'ssw_description'  : 'You forgot to fill this in'
    ,   'credit_value'     : 0
    ,   'bv_value'         : 0
    }

    def setUp(self):
        self.mech = MechDesign.objects.get(**self.__class__.mech_ident)

    def mech_compare(self, actual, expected, errorText):
        self.assertEqual(actual, expected, errorText % (self.mech.mech_name, self.mech.mech_code, expected, actual))

    def test_walkingMP(self):
        self.mech_compare(self.mech.move_walk(), self.__class__.movement_profile[0]
                          , '%s %s should have a walking MP of %i, got %i')

    def test_runningMP(self):
        self.mech_compare(self.mech.move_run(), self.__class__.movement_profile[1]
                          , '%s %s should have a running MP of %i, got %i')
        
    def test_jumpMP(self):
        self.mech_compare(self.mech.move_jump(), self.__class__.movement_profile[2]
                          , '%s %s should have a jumping MP of %i, got %i')
    
    def test_directFireTonnage(self):
        self.mech_compare(self.mech.directfire_tonnage(), self.__class__.directfire_tonnage
                         , '%s %s should have %i tons of direct fire weaponry, got %i') 

    def test_productionYear(self):
        self.mech_compare( self.mech.production_year, self.__class__.check_fields['production_year']
                         , 'The %s %s was produced in %i, got %i')

    def test_battleValue(self):
        self.mech_compare( self.mech.bv_value, self.__class__.check_fields['bv_value']
                         , 'The %s %s should have a battle value of %i, got %i')

    def test_creditValue(self):
        self.mech_compare( self.mech.credit_value, self.__class__.check_fields['credit_value']
                         , 'The %s %s should cost %i, got %i')

    def test_sswDescription(self):
        self.mech_compare( self.mech.ssw_description, self.__class__.check_fields['ssw_description']
                         , 'The %s %s description should be %s, got %s')

    def assertEquipment(self, location, slots, ssw_name):
        try:
            mount = self.mech.locations.get(location__location=location).criticals.get(slots=slots)
        except ObjectDoesNotExist:
            #Deliberately fail here, since apparently we couldn't find the object in these slots
            self.assertTrue(False, "Unable to find mounting in %s, slots %s" % (location, slots))

        mounted_name = mount.equipment.equipment.ssw_name
        self.assertEqual(mounted_name, ssw_name, "Object mounted in %s [%s] is %s, not %s" % (location, slots, mounted_name, ssw_name))

    def engine_checkXL(self, lt_slots='1,2,3', rt_slots='1,2,3'):
        self.assertEquipment('CT','1,2,3,8,9,10','Engine - XL Engine')
        self.assertEquipment('LT',lt_slots,'Engine - XL Engine')
        self.assertEquipment('RT',rt_slots,'Engine - XL Engine')

class Wolverine7DTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Wolverine'
    ,   'mech_code'    : 'WVR-7D'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,5]
    directfire_tonnage = 11
    check_fields = {
        'production_year'  : 3052
    ,   'ssw_description'  : 'Wolverine WVR-7D 55t, 5/8[10]/5 MASC, XLFE, Std; 10.0T/97% FF Armor; 13 SHS; 1 UAC5, 1 MPL, 1 SRM6'
    ,   'credit_value'     : 11214456
    ,   'bv_value'         : 1314
    }

    def test_hands(self):
        self.assertEquipment('LA','4','Actuator - Hand')
        self.assertEquipment('RA','4','Actuator - Hand')

    def test_engine(self):
        self.engine_checkXL(lt_slots='1,2,3', rt_slots='1,2,3')

    def test_engine(self):
        self.assertEquipment('CT','4,5,6,7','Gyro - Standard Gyro')

class Raven4LTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Raven'
    ,   'mech_code'    : 'RVN-4L'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [6,9,0]
    directfire_tonnage = 2
    check_fields = {
        'production_year'  : 3062
    ,   'ssw_description'  : 'Raven RVN-4L 35t, 6/9/0, XLFE, Std; 6.0T/81% Stlth Armor; 10 DHS; 1 ECM, 1 Narc, 2 ERML, 1 BAP, 1 SRM6, 1 TAG'
    ,   'credit_value'     : 6001425
    ,   'bv_value'         : 873
    }

class Dervish8DTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Dervish'
    ,   'mech_code'    : 'DV-8D'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,5]
    directfire_tonnage = 4
    check_fields = {
        'production_year'  : 3062
    ,   'ssw_description'  : 'Dervish DV-8D 55t, 5/8/5, XLFE, ES; 10.5T/91% Armor; 10 DHS; 2 LRM15, 4 ERML'
    ,   'credit_value'     : 10782316
    ,   'bv_value'         : 1765
    }

    def test_engine(self):
        self.engine_checkXL(lt_slots='1,2,3', rt_slots='1,2,3')

    def test_artemis(self):
        self.assertEquipment('LT','4,5,6','Equipment - (IS) LRM-15') 
        self.assertEquipment('LT','7','FCS - Artemis IV')
 
        self.assertEquipment('RT','4,5,6','Equipment - (IS) LRM-15') 
        self.assertEquipment('RT','7','FCS - Artemis IV')

class Griffin1NTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Griffin'
    ,   'mech_code'    : 'GRF-1N'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,5]
    directfire_tonnage = 7
    check_fields = {
        'production_year'  : 2492
    ,   'ssw_description'  : 'Griffin GRF-1N 55t, 5/8/5, Std FE, Std; 9.5T/82% Armor; 12 SHS; 1 PPC, 1 LRM10'
    ,   'credit_value'     : 4864106
    ,   'bv_value'         : 1272
    }

class Hatchetman3FTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Hatchetman'
    ,   'mech_code'    : 'HCT-3F'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [4,6,4]
    directfire_tonnage = 14
    check_fields = {
        'production_year'  : 3023
    ,   'ssw_description'  : 'Hatchetman HCT-3F 45t, 4/6/4, Std FE, Std; 6.5T/68% Armor; 11 SHS; 2 ML, 1 AC10, 1 Htcht'
    ,   'credit_value'     : 3111990
    ,   'bv_value'         : 854
    }

    def test_hatchet(self):
        self.assertEquipment('RA','5,6,7','Equipment - Hatchet')
