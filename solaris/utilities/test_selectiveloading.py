from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from solaris.warbook.mech.models import MechDesign

from solaris.utilities.loader import SSWLoader

class SelectiveLoadingTests(TestCase):
    ssw_filename = 'TestOwens OW-1.ssw'
    mechs_path   = 'data/test-mechs/'
    
    def setUp(self):
        self.loader = SSWLoader(self.__class__.ssw_filename, basepath=self.__class__.mechs_path)
        
        base_config = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Base')
        self.loadout = self.loader.load_single_loadout('LoadMe', base_config)

    def assertEquipment(self, design, location, slots, ssw_name):
        try:
            mount = design.locations.get(location__location=location).criticals.get(slots=slots)
        except ObjectDoesNotExist:
            listing = ""
            for item in design.locations.get(location__location=location).criticals.all().order_by('slots'):
                listing += '\t [%s] %s\n' % (item.slots, item.equipment.equipment.ssw_name)
            #Deliberately fail here, since apparently we couldn't find the object in these slots
            self.assertTrue(False, "Unable to find mounting in %s, slots %s. Location contains:\n%s" % (location, slots, listing))

        mounted_name = mount.equipment.equipment.ssw_name
        self.assertEqual(mounted_name, ssw_name, "Object mounted in %s [%s] is %s, not %s" % (location, slots, mounted_name, ssw_name))

    # The test mech re-arranges some of the equipment in the standard config
    # Check that the base hasn't been overwritten by checking for these changes
    def test_base_tag_unchanged(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Base') 
        
        self.assertEquipment(design, 'RT', '4', 'Equipment - TAG')
        
    def test_base_c3s_unchanged(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Base') 
        
        self.assertEquipment(design, 'RT', '5', 'Equipment - C3 Computer (Slave)')
        
    # The Prime config in the file has no weapons and an incorrect battle-value. Make sure it hasn't been
    # overwritten by checking for the correct configuration.    
    def test_prime_bv_unchanged(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Prime') 
        
        self.assertEqual(design.bv_value, 839, "Prime config should have a BV of 839, found %d" % design.bv_value)
        
    def test_prime_hd_medlaser(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Prime') 
                
        self.assertEquipment(design, 'HD', '4', 'Equipment - (IS) Medium Laser')
        
    # Check that LoadMe was loaded and links correctly to the base chassis
    def test_loadme_exists(self):
        count = MechDesign.objects.filter(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe').count()
        
        self.assertEquals(count, 1, 'Expected to find Owens OW-1 LoadMe Test Config, found none')
        
    def test_loadme_baseconfig(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe')
        base_design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Base') 
        
        self.assertEquals(design.omni_basechassis, base_design, 'Owens Test config has incorrect base design')
        
    def test_loadme_returned(self):
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe')
        self.assertNotEquals(self.loadout.id, design.id, 'Loader Returned Mech does not match mech in Database')
        
    # Check that DontLoad wasn't loaded
    def test_donload_not_exists(self):
        count = MechDesign.objects.filter(mech_name='Owens',mech_code='OW-1',omni_loadout='DontLoad').count()
        
        self.assertEquals(count, 0, 'Expected to not to find Owens OW-1 DontLoad Test Config, found in database')
    
        
 
        
        