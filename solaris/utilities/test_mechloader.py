from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from solaris.utilities.loader import SSWLoader
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.equipment.models import MechEquipment

engineLayout = {
    'Fusion' : {
        'engine' : 'Engine - Fusion Engine'
    ,   'slots'  : { 'CT' : '1,2,3,8,9,10' }
    }
,   'XL' : {
        'engine' : 'Engine - XL Engine'
    ,   'slots'  : { 'CT' : '1,2,3,8,9,10', 'LT' : '1,2,3', 'RT' : '1,2,3' }
    }
,   'Light' : {
        'engine' : 'Engine - Light Fusion Engine'
    ,   'slots'  : { 'CT' : '1,2,3,8,9,10', 'LT' : '1,2', 'RT' : '1,2' }
    }
}

gyroLayout = {
    'Standard' : {
        'gyro'  : 'Gyro - Standard Gyro'
    ,   'slots' : '4,5,6,7'
    }
,   'XL' : {
        'gyro'  : 'Gyro - Extra-Light Gyro'
    ,   'slots' : '4,5,6,7,8,9'
    }
,   'Compact' : {
        'gyro'  : 'Gyro - Compact Gyro'
    ,   'slots' : '4,5'
    }
}

cockpitLayout = {
    'Standard' : {
        'cockpit' : { 'type' : 'Cockpit - Standard Cockpit' 
                    , 'slots' : [ ('HD', '3') ]
                    }
    ,   'sensors' : { 'type' : 'Cockpit - Sensors' 
                    , 'slots' : [ ('HD', '2'), ('HD', '5') ]
                    }
    ,   'support' : { 'type' : 'Cockpit - Life Support' 
                    , 'slots' : [ ('HD', '1'), ('HD', '6') ]
                    }
    }
,   'Small' : {
        'cockpit' : { 'type' : 'Cockpit - Small Cockpit' 
                    , 'slots' : [ ('HD', '3') ]
                    }
    ,   'sensors' : { 'type' : 'Cockpit - Sensors' 
                    , 'slots' : [ ('HD', '2'), ('HD', '4') ]
                    }
    ,   'support' : { 'type' : 'Cockpit - Life Support' 
                    , 'slots' : [ ('HD', '1') ]
                    }
    }
}


mechLocations = {
    'Biped' : ('LA','RA','RL','LL','RT','CT','LT','HD','--', 'RCT','RRT','RLT')
,   'Quad'  : ('LFL','RFL','RRL','LRL','RT','CT','LT','HD','--', 'RCT','RRT','RLT')
}

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
    engine = engineLayout['Fusion']
    gyro = gyroLayout['Standard']
    cockpit = cockpitLayout['Standard']
    locations = mechLocations['Biped']

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
        self.assertEquipment('CT', self.__class__.gyro['slots'], self.__class__.gyro['gyro'])

    def test_engine(self):
        for (location, slots) in self.__class__.engine['slots'].items():
            self.assertEquipment(location, slots, self.__class__.engine['engine'])

    def test_expectedLocations(self):
        count = self.mech.locations.filter(location__location__in=self.locations).count()
        self.assertEqual( count
                           , len(self.locations)
                           , 'Location check found %i of %i expected locations' % (count, len(self.locations))
                           )

    def test_unexpectedLocations(self):
        count = self.mech.locations.exclude(location__location__in=self.locations).count()
        self.assertEqual(count, 0, 'Location check, found %i unexpected limbs' % count)

    def test_cockpit(self):
        cockpit = self.cockpit['cockpit']
        for (location, slot) in cockpit['slots']:
            self.assertEquipment(location, slot, cockpit['type'])

    def test_sensors(self):
        sensors = self.cockpit['sensors']
        for (location, slot) in sensors['slots']:
            self.assertEquipment(location, slot, sensors['type'])

    def test_lifeSupport(self):
        support = self.cockpit['support']
        for (location, slot) in support['slots']:
            self.assertEquipment(location, slot, support['type'])

    def assertEquipment(self, location, slots, ssw_name):
        try:
            mount = self.mech.locations.get(location__location=location).criticals.get(slots=slots)
        except ObjectDoesNotExist:
            listing = ""
            for item in self.mech.locations.get(location__location=location).criticals.all().order_by('slots'):
                listing += '\t [%s] %s\n' % (item.slots, item.equipment.equipment.ssw_name)
            #Deliberately fail here, since apparently we couldn't find the object in these slots
            self.assertTrue(False, "Unable to find mounting in %s, slots %s. Location contains:\n%s" % (location, slots, listing))

        mounted_name = mount.equipment.equipment.ssw_name
        self.assertEqual(mounted_name, ssw_name, "Object mounted in %s [%s] is %s, not %s" % (location, slots, mounted_name, ssw_name))

class LoadedMechTestMixin(MechTestMixin):
    ssw_filename = 'TestMech.ssw'
    mechs_path   = 'data/test-mechs/'

    def setUp(self):
        self.loader = SSWLoader(self.__class__.ssw_filename, basepath=self.__class__.mechs_path)
        self.loader.load_mechs(print_message=False)
        super(LoadedMechTestMixin, self).setUp()

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
    engine = engineLayout['XL']

    def test_hands(self):
        self.assertEquipment('LA','4','Actuator - Hand')
        self.assertEquipment('RA','4','Actuator - Hand')

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
    engine = engineLayout['XL']

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
    engine = engineLayout['XL']

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
    engine = engineLayout['XL']

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
    engine = engineLayout['XL']

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
    engine = engineLayout['Light']

    def test_targetingComputer(self):
        self.assertEquipment('LT','3,4,5,6,7,8,9','Equipment - (IS) Targeting Computer')

    def test_gaussRifle(self):
        self.assertEquipment('RA','4,5,6,7,8,9,10','Equipment - (IS) Gauss Rifle')

class Cuirass1XTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Cuirass'
    ,   'mech_code'    : 'CDR-1X'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [6,9,6]
    directfire_tonnage = 11
    check_fields = {
        'production_year'  : 3085
    ,   'ssw_description'  : 'Cuirass CDR-1X 40t, 6/9/6, XLFE, ES, XL Gyro; 8.0T/93% Armor; 10 SHS; 1 RAC5, 1 ERML, 1 Swrd'
    ,   'credit_value'     : 6993280
    ,   'bv_value'         : 1301
    }
    engine = {
        'engine' : 'Engine - XL Engine'
    ,   'slots'  : { 'CT' : '1,2,3,10,11,12', 'LT' : '1,2,3', 'RT' : '1,2,3' }
    }
    gyro = gyroLayout['XL']

    def test_sword(self):
        self.assertEquipment('RA','5,6,7','Equipment - Sword')

    def test_rotaryAC(self):
        self.assertEquipment('LA','4,5,6,7,8,9','Equipment - (IS) Rotary AC/5')

class Sirocco6CTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Sirocco'
    ,   'mech_code'    : 'SRC-6C'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [3,5,5]
    directfire_tonnage = 21
    check_fields = {
        'production_year'  : 3070
    ,   'ssw_description'  : 'Sirocco SRC-6C 95t, 3/5/5, Std FE, Std Quad; 18.5T/100% LFF Armor; 10 DHS; 1 ECM, 1 ERLL, 1 C3S, 4 ERML, 1 LGR'
    ,   'credit_value'     : 12189450
    ,   'bv_value'         : 2202
    }
    cockpit = cockpitLayout['Small']
    locations = mechLocations['Quad']

    def test_leftForeLeg(self):
        self.assertEquipment('LFL','1','Actuator - Hip')

    def test_rightForeLeg(self):
        self.assertEquipment('RFL','2','Actuator - Upper Leg')

    def test_leftRearLeg(self):
        self.assertEquipment('LRL','3','Actuator - Lower Leg')

    def test_rightRearLeg(self):
        self.assertEquipment('RRL','4','Actuator - Foot')

class Quickdraw8XTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Quickdraw'
    ,   'mech_code'    : 'QKD-8X'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,0]
    directfire_tonnage = 9
    check_fields = {
        'production_year'  : 3073
    ,   'ssw_description'  : 'Quickdraw QKD-8X 60t, 5[6]/8[9]/0 TSM, Std FE, ES, Cmp Gyro; 12.0T/96% Stlth Armor; 12 SHS; 2 ML, 1 ECM, 1 PPC, 1 LftHst, 1 TAG'
    ,   'credit_value'     : 9903360
    ,   'bv_value'         : 1580
    }
    engine = {
        'engine' : 'Engine - Fusion Engine'
    ,   'slots'  : { 'CT' : '1,2,3,6,7,8' } 
    }
    gyro = gyroLayout['Compact']

    cockpit = {
        'cockpit' : { 'type' : 'Cockpit - Torso-Mounted Cockpit' 
                    , 'slots' : [ ('CT', '9') ]
                    }
    ,   'sensors' : { 'type' : 'Cockpit - Sensors' 
                    , 'slots' : [ ('HD', '1'), ('HD', '2'), ('CT', '10') ]
                    }
    ,   'support' : { 'type' : 'Cockpit - Life Support' 
                    , 'slots' : [ ('RT', '1'), ('LT', '1') ]
                    }
    }

    def test_turret(self):
        self.assertEquipment('CT', '11', 'Turret - Head Turret')

    def test_turretLocation(self):
        # Gives a more meaningful error message, and I know there's only one turret.
        turret = MechEquipment.objects.get(mech=self.mech, equipment__ssw_name__contains='Turret')
        for mount in turret.mountings.all():
            self.assertEqual(mount.location.location.location
                            , 'CT', 'Expected to find Turret on Centre Torso, found on %s'
                            % mount.location.location.location
                            )

    def test_turretSlot(self):
        # Gives a more meaningful error message, and I know there's only one turret.
        turret = MechEquipment.objects.get(mech=self.mech, equipment__ssw_name__contains='Turret')
        for mount in turret.mountings.all():
            self.assertEqual(mount.slots
                            , '11', 'Expected to find Turret on slot 11, found in %s'
                            % mount.slots
                            )

    def test_stealthArmour(self):
        for (location, slots) in [ ('RA', '11,12'), ('RT','10,11'), ('RL', '5,6')
                                 , ('LA', '11,12'), ('LT','9,10'), ('LL', '5,6') ]:
            self.assertEquipment(location, slots, 'Armour - Stealth Armor')

    def test_liftHoist(self):
        self.assertEquipment('LT', '2,3,4', 'Equipment - Lift Hoist')

    def test_liftHoistRear(self):
        try:
            hoist = self.mech.locations.get(location__location='LT').criticals.get(slots='2,3,4')
            self.assertTrue(hoist.rear_firing, 'Hoist should be mounted as rear facing')
        except ObjectDoesNotExist:
            self.assertTrue(False, 'Unable to locate lift hoist')

    def test_turretTonnage(self):
        head = self.mech.locations.get(location__location='HD')
        self.assertEqual( head.turret_tonnage(), 7.0
                           , 'Expected combined tonnage of head equipment to be %.1f, got %.1f' 
                           % ( 7.0, head.turret_tonnage() )
                           )

    def test_turretItemTonnage(self):
        turret = MechEquipment.objects.get(mech=self.mech, equipment__ssw_name__contains='Turret')
        self.assertNotEqual(turret.tonnage(), 1.0, 'Expected turret tonnage to be 1.0 Tons, got %.1f' % turret.tonnage())

class Hunchback6STests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Hunchback'
    ,   'mech_code'    : 'HBK-6S'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [6,9,0]
    directfire_tonnage = 16
    check_fields = {
        'production_year'  : 3063
    ,   'ssw_description'  : 'Hunchback HBK-6S 50t, 6/9/0, XLFE, ES; 10.0T/95% Armor; 10 DHS; 2 ERML, 1 SRM6, 1 LB20'
    ,   'credit_value'     : 9732000
    ,   'bv_value'         : 1380
    }
    engine = engineLayout['XL']

    def test_lb20Centre(self):
        self.assertEquipment('CT', '11,12', 'Equipment - (IS) LB 20-X AC')

    def test_lb20Right(self):
        self.assertEquipment('RT', '4,5,6,7,8,9,10,11,12', 'Equipment - (IS) LB 20-X AC')

class Jenner10XTests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Jenner'
    ,   'mech_code'    : 'JR10-X'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [7,11,7]
    directfire_tonnage = 6
    check_fields = {
        'production_year'  : 3072
    ,   'ssw_description'  : 'Jenner JR10-X 35t, 7/11/7, XLFE, Comp, Cmp Gyro; 7.0T/99% LFF Armor; 10 DHS; 6 ML, 1 AECM, NullSig'
    ,   'credit_value'     : 10748925
    ,   'bv_value'         : 1452
    }
    engine = {
        'engine' : 'Engine - XL Engine'
    ,   'slots'  : { 'CT' : '1,2,3,6,7,8'
                   , 'LT' : '2,3,4'
                   , 'RT' : '2,3,4' } 
    }
    gyro = gyroLayout['Compact']

    cockpit = {
        'cockpit' : { 'type' : 'Cockpit - Torso-Mounted Cockpit' 
                    , 'slots' : [ ('CT', '9') ]
                    }
    ,   'sensors' : { 'type' : 'Cockpit - Sensors' 
                    , 'slots' : [ ('HD', '1'), ('HD', '2'), ('CT', '10') ]
                    }
    ,   'support' : { 'type' : 'Cockpit - Life Support' 
                    , 'slots' : [ ('RT', '1'), ('LT', '1') ]
                    }
    }

    def test_nullsigCT(self):
        self.assertEquipment('CT', '12', 'Multislot - Null Signature System')

    def test_nullsigRT(self):
        self.assertEquipment('RT', '10', 'Multislot - Null Signature System')

    def test_nullsigLT(self):
        self.assertEquipment('LT', '11', 'Multislot - Null Signature System')

    def test_nullsigLA(self):
        self.assertEquipment('LA', '5', 'Multislot - Null Signature System')

    def test_nullsigRA(self):
        self.assertEquipment('RA', '5', 'Multislot - Null Signature System')

    def test_nullsigRL(self):
        self.assertEquipment('RL', '5', 'Multislot - Null Signature System')

    def test_nullsigLL(self):
        self.assertEquipment('LL', '5', 'Multislot - Null Signature System')

class Whitworth5STests(MechTestMixin, TestCase):
    mech_ident = {
        'mech_name'    : 'Whitworth'
    ,   'mech_code'    : 'WTH-5S'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [4,6,4]
    directfire_tonnage = 4
    check_fields = {
        'production_year'  : 3074
    ,   'ssw_description'  : 'Whitworth WTH-5S 40t, 4/6[8]/4, XLFE, Comp; 8.0T/93% Armor; 10 DHS; 1 ECM, 2 MXPL, 2 SSRM6'
    ,   'credit_value'     : 7789133
    ,   'bv_value'         : 1320
    }
    engine = engineLayout['XL']

    def test_rightArmAES(self):
        self.assertEquipment('RA', '5,6', 'AES - Arm AES')

    def test_leftArmAES(self):
        self.assertEquipment('LA', '8,9', 'AES - Arm AES')

class AESQuadMechTests(LoadedMechTestMixin, TestCase):
    ssw_filename = 'QuadAESTest QAT-1.ssw'
    mech_ident = {
        'mech_name'    : 'QuadAESTest'
    ,   'mech_code'    : 'QAT-1'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,0]
    directfire_tonnage = 5
    check_fields = {
        'production_year'  : 2750
    ,   'ssw_description'  : 'QuadAESTest QAT-1 55t, 5/8/0, Std FE, Std Quad; 11.5T/92% Armor; 10 SHS; 1 SSRM6, 1 LL'
    ,   'credit_value'     : 4597816
    ,   'bv_value'         : 1218
    }
    locations = mechLocations['Quad']

    def test_rightForeAES(self):
        self.assertEquipment('RFL', '5,6', 'AES - Leg AES (Quad)')

    def test_leftForeAES(self):
        self.assertEquipment('LFL', '5,6', 'AES - Leg AES (Quad)')

    def test_rightRearAES(self):
        self.assertEquipment('RRL', '5,6', 'AES - Leg AES (Quad)')

    def test_leftRearAES(self):
        self.assertEquipment('LRL', '5,6', 'AES - Leg AES (Quad)')

class AESBipedMechTests(LoadedMechTestMixin, TestCase):
    ssw_filename = 'BipedAESTest BAT-1.ssw'
    mech_ident = {
        'mech_name'    : 'BipedAESTest'
    ,   'mech_code'    : 'BAT-1'
    ,   'omni_loadout' : 'Base'
    }
    movement_profile = [5,8,0]
    directfire_tonnage = 5
    check_fields = {
        'production_year'  : 2750
    ,   'ssw_description'  : 'BipedAESTest BAT-1 35t, 5/8/0, Std FE, Std; 7.0T/94% Armor; 10 DHS; 1 LL, 1 SSRM6'
    ,   'credit_value'     : 2500110
    ,   'bv_value'         : 843
    }
    locations = mechLocations['Biped']

    def test_rightLegAES(self):
        self.assertEquipment('RL', '5', 'AES - Leg AES (Biped)')

    def test_leftForeAES(self):
        self.assertEquipment('LL', '5', 'AES - Leg AES (Biped)')

