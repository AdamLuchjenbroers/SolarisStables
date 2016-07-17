from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

import json

from solaris.stablemanager.tests import StableTestMixin
from solaris.warbook.mech.models import MechDesign

from solaris.files.models import TempMechFile

class UploadNotLoggedInTest(TestCase):
    def test_try_get(self):
        client = Client()
        
        response = client.get('/stable/mechs/upload/purchase')
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from page (HTTP %s)' % response.status_code)
    
    def test_try_post(self):
        client = Client()
        ssw = SimpleUploadedFile('MockMechData.ssw', 'No Valid Data!')
        
        response = client.post('/stable/mechs/upload/purchase', {'ssw_file' : ssw})
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from page (HTTP %s)' % response.status_code)
        
class IncorrectFormTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')
        
    def test_missing_mech(self):
        response = self.client.post('/stable/mechs/upload/purchase')
        
        self.assertEqual(response.status_code, 400, 'Form without mech returns incorrect status code (HTTP %s)' % response.status_code)
        
    def test_junk_mechfile(self):
        ssw = SimpleUploadedFile('JunkMechData.ssw', 'Not A Valid SSW File!')
        response = self.client.post('/stable/mechs/upload/purchase', {'ssw_file' : ssw})
        
        self.assertEqual(response.status_code, 400, 'Form with incorrect mechfile returns incorrect status code (HTTP %s)' % response.status_code)
        
        
class UploadMechsMixin(StableTestMixin):
    ssw_filename = 'TestMech.ssw'
    mechs_path   = 'data/test-mechs/'

    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')
        
        filename = '%s%s' % (self.__class__.mechs_path, self.__class__.ssw_filename)
        
        with open(filename, 'rb') as ssw_data:
            self.response = self.client.post('/stable/mechs/upload/purchase', {'ssw_file' : ssw_data})
        
        self.json_data = json.loads(self.response.content)

    def compare_by_key(self, key, errorstring):
        if 'exception' in self.json_data:
            self.assertFalse(True, 'Query failed due to %s' % self.json_data['exception'])
        
        self.assertEqual(self.expect[key], self.json_data[key], errorstring % (self.expect[key], self.json_data[key]))
        
    def test_assigned_id(self):
        self.assertIn('temp_id', self.json_data, 'No Temporary Mech Identifier returned')

    def test_mech_name(self):
        self.compare_by_key('mech_name', 'Incorrect Mech Name: expected %s, got %s')     

    def test_mech_code(self):
        self.compare_by_key('mech_code', 'Incorrect Mech Code: expected %s, got %s')     

    def test_is_omni(self):
        self.compare_by_key('is_omni', 'Incorrect Omni Status: expected %s, got %s')     

    def test_tonnage(self):
        self.compare_by_key('tons', 'Incorrect Tonnage: expected %s, got %s')     

    def test_bv(self):
        self.compare_by_key('bv', 'Incorrect Battle Value: expected %s, got %s')     

    def test_cost(self):
        self.compare_by_key('cost', 'Incorrect Cost: expected %s, got %s')     

    def test_motive_type(self):
        self.compare_by_key('motive_type', 'Incorrect Motive Type: expected %s, got %s')     

    def test_techbase(self):
        self.compare_by_key('techbase', 'Incorrect Technology Base: expected %s, got %s')     

    def test_design_status(self):
        self.compare_by_key('design_status', 'Incorrect Design Status Code: expected %s, got %s')     

    def test_design_status_text(self):
        self.compare_by_key('design_status_text', 'Incorrect Design Status Text: expected %s, got %s')            
         
    def test_request_successful(self):
        self.assertEqual(self.response.status_code, 200, 'Submission unsuccessful for a logged in user (HTTP %s)' % self.response.status_code)
    

class NewSimpleUploadTests(UploadMechsMixin, TestCase):    
    ssw_filename = 'SimpleLoadingTest SLT-1.ssw'    
    expect = {
        'mech_name' : 'SimpleLoadingTest' 
      , 'mech_code' : 'SLT-1'
      , 'is_omni'   : False
      , 'tons'      : 50
      , 'bv'        : 1167 
      , 'cost'      : 4029500 
      , 'motive_type' : 'Biped'
      , 'techbase'  : 'Inner Sphere' 
      , 'design_status' : 'N'
      , 'design_status_text' : 'New Design'
    }

    def test_has_no_loadouts(self):
        self.assertNotIn('loadouts', self.json_data, 'Loadout List Found for Non-Omnimech')
    
class ExistingSimpleUploadTests(StableTestMixin, TestCase):    

    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')
        
        with open('data/test-mechs/TestWolverine WVR-6K.ssw', 'rb') as ssw_data:
            self.response = self.client.post('/stable/mechs/upload/purchase', {'ssw_file' : ssw_data})
        
    def test_upload_rejected(self):        
        self.assertEqual(self.response.status_code, 400, 'Upload of existing mech design returns incorrect status code (HTTP %s)' % self.response.status_code)   

class NewOmniUploadTests(UploadMechsMixin, TestCase):    
    ssw_filename = 'OmniLoadingTest OLT-1.ssw'
    expect = {
        'mech_name' : 'OmniLoadingTest' 
      , 'mech_code' : 'OLT-1'
      , 'is_omni'   : True
      , 'tons'      : 30
      , 'bv'        : None 
      , 'cost'      : 3049312
      , 'motive_type' : 'Biped'
      , 'techbase'  : 'Inner Sphere' 
      , 'design_status' : 'N'
      , 'design_status_text' : 'New Design'
      , 'num_loadouts' : 3
    }

    def test_has_loadouts(self):
        self.assertIn('loadouts', self.json_data, 'Loadout List Not Found')
        
    def test_loadout_count(self):
        self.compare_by_key('num_loadouts', 'Incorrect Loadout Count: expected %s, got %s')

    def test_configA_exists(self):
        self.assertIn('A', self.json_data['loadouts'], 'Config A not found')

    def test_configA_cost(self):
        cost = self.json_data['loadouts']['A']['cost']
        expect = 3274781
        self.assertEqual(cost, expect, 'Cost for config A is %s, expected %s' % (cost, expect))

    def test_configA_bv(self):
        cost = self.json_data['loadouts']['A']['bv']
        expect = 814
        self.assertEqual(cost, expect, 'Battle Value for config A is %s, expected %s' % (cost, expect))

    def test_configB_exists(self):
        self.assertIn('B', self.json_data['loadouts'], 'Config B not found')

    def test_configB_cost(self):
        cost = self.json_data['loadouts']['B']['cost']
        expect = 3110250
        self.assertEqual(cost, expect, 'Cost for config B is %s, expected %s' % (cost, expect))

    def test_configB_bv(self):
        cost = self.json_data['loadouts']['B']['bv']
        expect = 700
        self.assertEqual(cost, expect, 'Battle Value for config B is %s, expected %s' % (cost, expect))

    def test_configC_exists(self):
        self.assertIn('C', self.json_data['loadouts'], 'Config C not found')

    def test_configC_cost(self):
        cost = self.json_data['loadouts']['C']['cost']
        expect = 3049312
        self.assertEqual(cost, expect, 'Cost for config C is %s, expected %s' % (cost, expect))

    def test_configC_bv(self):
        cost = self.json_data['loadouts']['C']['bv']
        expect = 747
        self.assertEqual(cost, expect, 'Battle Value for config C is %s, expected %s' % (cost, expect))
        

class ExistingOmniUploadTests(UploadMechsMixin, TestCase):    
    ssw_filename = 'TestOwens OW-1.ssw'
    expect = {
        'mech_name' : 'Owens' 
      , 'mech_code' : 'OW-1'
      , 'is_omni'   : True
      , 'tons'      : 35
      , 'bv'        : None 
      , 'cost'      : 7625531
      , 'motive_type' : 'Biped'
      , 'techbase'  : 'Inner Sphere' 
      , 'design_status' : 'P'
      , 'design_status_text' : 'Standard Production Design'
      , 'num_loadouts' : 2
    }
    
    def setUp(self):
        super(ExistingOmniUploadTests, self).setUp()
        
        self.tempmech = TempMechFile.objects.get(id=self.json_data['temp_id'])

    def assertDesignStatus(self, loadout, expect):
        design_status = self.json_data['loadouts'][loadout]['design_status']
        self.assertEqual(design_status, expect, 'Design Status Code for config %s is %s, expected %s' % (loadout, design_status, expect))       

    def assertDesignStatusText(self, loadout, expect):
        design_status = self.json_data['loadouts'][loadout]['design_status_text']
        self.assertEqual(design_status, expect, 'Design Status Text for config %s is %s, expected %s' % (loadout, design_status, expect)) 
        
    def test_has_loadouts(self):
        self.assertIn('loadouts', self.json_data, 'Loadout List Not Found')
        
    def test_loadout_count(self):
        self.compare_by_key('num_loadouts', 'Incorrect Loadout Count: expected %s, got %s')
        
    def test_production_config_removed(self):
        self.assertNotIn('Prime', self.json_data['loadouts'], 'Production configurations should be excluded from available uploads')
   
    def test_loadme_config_status(self):
        self.assertDesignStatus('LoadMe','N')
        
    def test_loadme_config_status_text(self):
        self.assertDesignStatusText('LoadMe','New Design')
        
    def test_dontload_config_status(self):
        self.assertDesignStatus('DontLoad','N')
        
    def test_dontload_config_status_text(self):
        self.assertDesignStatusText('DontLoad','New Design')
        
    def test_loadmech_newconfig(self):
        config = self.tempmech.load_config('LoadMe')
        self.assertIsNotNone(config.id, 'Loadme Config not loaded, no ID allocated')
                          
    # Check that LoadMe was loaded and links correctly to the base chassis
    def test_loadme_exists(self):
        config = self.tempmech.load_config('LoadMe')
        count = MechDesign.objects.filter(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe').count()
        
        self.assertEquals(count, 1, 'Expected to find Owens OW-1 LoadMe Test Config, found none')
        
    def test_loadme_baseconfig(self):
        config = self.tempmech.load_config('LoadMe')
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe')
        base_design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='Base') 
        
        self.assertEquals(design.omni_basechassis, base_design, 'Owens Test config has incorrect base design')
        
    def test_loadme_returned(self):
        config = self.tempmech.load_config('LoadMe')
        design = MechDesign.objects.get(mech_name='Owens',mech_code='OW-1',omni_loadout='LoadMe')
        self.assertEquals(config.id, design.id, 'Loader Returned Mech does not match mech in Database')
        
    # Check that DontLoad wasn't loaded
    def test_donload_not_exists(self):
        config = self.tempmech.load_config('LoadMe')
        count = MechDesign.objects.filter(mech_name='Owens',mech_code='OW-1',omni_loadout='DontLoad').count()
        
        self.assertEquals(count, 0, 'Expected to not to find Owens OW-1 DontLoad Test Config, found in database')
        
        