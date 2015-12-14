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
                         , '%s %s should have %.1f tons of direct fire weaponry, got %.1f') 

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

    def test_gyro(self):
        self.assertEquipment('CT','4,5,6,7','Gyro - Standard Gyro')

    def assertEquipment(self, location, slots, ssw_name):
        try:
            mount = self.mech.locations.get(location__location=location).criticals.get(slots=slots)
        except ObjectDoesNotExist:
            #Deliberately fail here, since apparently we couldn't find the object in these slots
            self.assertTrue(False, "Unable to find mounting in %s, slots %s" % (location, slots))

        mounted_name = mount.equipment.equipment.ssw_name
        self.assertEqual(mounted_name, ssw_name, "Object mounted in %s [%s] is %s, not %s" % (location, slots, mounted_name, ssw_name))

    def engine_checkGeneric(self, lt_slots=None, rt_slots=None, ct_slots='1,2,3,8,9,10', engine='Engine - Fusion Engine'):
        self.assertEquipment('CT', ct_slots, engine)
        if lt_slots != None:
           self.assertEquipment('LT', lt_slots, engine)
        if rt_slots != None:
           self.assertEquipment('RT', rt_slots, engine)

    def engine_checkXL(self, lt_slots='1,2,3', rt_slots='1,2,3'):
        self.engine_checkGeneric(lt_slots=lt_slots, rt_slots=rt_slots, engine = 'Engine - XL Engine')

    def engine_checkLight(self, lt_slots='1,2', rt_slots='1,2'):
        self.check_Generic(lt_slots=lt_slots, rt_slots=rt_slots, engine = 'Engine - Light Fusion Engine')

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

class OwensOW1BaseTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Owens'
    ,   'mech_code'    : 'OW-1'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [8,12,0]
    directfire_tonnage = 0
    check_fields = {
        'production_year'  : 3056
    ,   'ssw_description'  : 'Owens OW-1 35t, 8/12/0, XLFE, Std; 7.0T/94% Armor; 10 SHS; 1 C3S, 1 BAP, 1 TAG'
    ,   'credit_value'     : 7832250
    ,   'bv_value'         : 0
    }

    def test_beagle(self):
        self.assertEquipment('LT','4,5','Equipment - Beagle Active Probe')

    def test_tag(self):
        self.assertEquipment('RT','4','Equipment - TAG')

    def test_c3Slave(self):
        self.assertEquipment('RT','5','Equipment - C3 Computer (Slave)')

class OwensOW1CTests(OwensOW1BaseTests):
    mech_ident = {
        'mech_name'    : 'Owens'
    ,   'mech_code'    : 'OW-1'
    ,   'omni_loadout' : 'C'
    }
    directfire_tonnage = 7
    check_fields = {
        'production_year'  : 3056
    ,   'ssw_description'  : 'Owens OW-1 C 35t, 8/12/0, XLFE, Std; 7.0T/94% Armor; 10 SHS; 2 ML, 1 C3S, 1 BAP, 1 TAG, 1 LL'
    ,   'credit_value'     : 7929281
    ,   'bv_value'         : 964
    }

    def test_largeLaser(self):
        self.assertEquipment('LA','3,4','Equipment - (IS) Large Laser')

    def test_mediumLaser(self):
        self.assertEquipment('RA','3','Equipment - (IS) Medium Laser')

class OwensOW1FTests(OwensOW1BaseTests):
    mech_ident = {
        'mech_name'    : 'Owens'
    ,   'mech_code'    : 'OW-1'
    ,   'omni_loadout' : 'F'
    }
    directfire_tonnage = 4
    check_fields = {
        'production_year'  : 3068
    ,   'ssw_description'  : 'Owens OW-1 F 35t, 8/12/0, XLFE, Std; 7.0T/94% Armor; 10 SHS; 1 ECM, 1 APod, 1 C3S, 2 ERSL, 1 BAP, 1 LPPC, 1 TAG, TC'
    ,   'credit_value'     : 8273531
    ,   'bv_value'         : 933
    }

    def test_targetingComputer(self):
        self.assertEquipment('HD','4','Equipment - (IS) Targeting Computer')

    def test_guardianECM(self):
        self.assertEquipment('LT','6,7','Equipment - Guardian ECM Suite')

    def test_lightPPC(self):
        self.assertEquipment('CT','11,12','Equipment - (IS) Light PPC')


class ExcaliburEXCCSTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Excalibur'
    ,   'mech_code'    : 'EXC-CS'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,0]
    directfire_tonnage = 11.5
    check_fields = {
        'production_year'  : 3067
    ,   'ssw_description'  : 'Excalibur EXC-CS 70t, 5[6]/8[9]/0 TSM, XLFE, ES; 13.5T/100% Armor; 12 DHS; 4 ERML, 1 ERSL, 1 ERPPC, 1 LRM20, TC'
    ,   'credit_value'     : 18188611
    ,   'bv_value'         : 2174
    }

    def test_targetingComputer(self):
        self.assertEquipment('LT','10,11,12','Equipment - (IS) Targeting Computer')

    def test_LRM20(self):
        self.assertEquipment('LT','4,5,6,7,8','Equipment - (IS) LRM-20')
    
    def test_artemisIV(self):
        self.assertEquipment('LT','9','FCS - Artemis IV')

    def test_tsmLA(self):
        self.assertEquipment('LA','10,11','Enhancement - TSM')

    def test_tsmRA(self):
        self.assertEquipment('RA','11,12','Enhancement - TSM')

    def test_tsmLegs(self):
        self.assertEquipment('RL','6','Enhancement - TSM')
        self.assertEquipment('LL','6','Enhancement - TSM')

class Gallowglas3GLSTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Gallowglas'
    ,   'mech_code'    : 'GAL-3GLS'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [4,6,0]
    directfire_tonnage = 26
    check_fields = {
        'production_year'  : 3064
    ,   'ssw_description'  : 'Gallowglas GAL-3GLS 70t, 4[5]/6[8]/0 TSM, LFE, ES; 13.0T/96% Armor; 10 DHS; 2 ERLL, 1 ERML, 1 GR, TC'
    ,   'credit_value'     : 12932920
    ,   'bv_value'         : 2291
    }

    def test_targetingComputer(self):
        self.assertEquipment('LT','3,4,5,6,7,8,9','Equipment - (IS) Targeting Computer')

    def test_gaussRifle(self):
        self.assertEquipment('RA','4,5,6,7,8,9,10','Equipment - (IS) Gauss Rifle')

