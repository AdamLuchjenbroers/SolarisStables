from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

import json

from solaris.stablemanager.tests import StableTestMixin
from solaris.warbook.mech.models import MechDesign

from solaris.files.models import TempMechFile

class RefitUploadNotLoggedInTest(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.stablemech = self.addMech(self.stable, mech_name='Owens', mech_code='OW-1', omni_loadout='C')
        self.stablemechweek = self.stablemech.get_mechweek()
        self.refit_url = self.stablemechweek.refit_url()

    def test_try_get(self):
        client = Client()
        
        response = client.get(self.refit_url)
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from page (HTTP %s)' % response.status_code)
    
    def test_try_post(self):
        client = Client()
        ssw = SimpleUploadedFile('MockMechData.ssw', 'No Valid Data!')
        
        response = client.get(self.refit_url)
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from page (HTTP %s)' % response.status_code)
        
class RefitIncorrectFormTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')

        self.stablemech = self.addMech(self.stable, mech_name='Owens', mech_code='OW-1', omni_loadout='C')
        self.stablemechweek = self.stablemech.get_mechweek(loadout='C')

        self.refit_url  = reverse('upload_loadout_mech', kwargs={'smw_id' : self.stablemechweek.id})

    def upload_mech(self, filename):
        with open(filename, 'rb') as ssw_data:
            response = self.client.post(self.refit_url, {'ssw_file' : ssw_data})

        return json.loads(response.content)
        
    def test_missing_mech(self):
        response = self.client.post(self.refit_url)
        
        self.assertEqual(response.status_code, 400, 'Form without mech returns incorrect status code (HTTP %s)' % response.status_code)
        
    def test_junk_mechfile(self):
        ssw = SimpleUploadedFile('JunkMechData.ssw', 'Not A Valid SSW File!')
        response = self.client.post(self.refit_url, {'ssw_file' : ssw})
        
        self.assertEqual(response.status_code, 400, 'Form with incorrect mechfile returns incorrect status code (HTTP %s)' % response.status_code)

    def test_wrong_mechfile(self):
        filename = 'data/test-mechs/OmniLoadingTest OLT-1.ssw'
        
        with open(filename, 'rb') as ssw_data:
            response = self.client.post(self.refit_url, {'ssw_file' : ssw_data})
        
        self.assertEqual(response.status_code, 400, 'Form with incompatible mech returns incorrect status code (HTTP %s)' % response.status_code)
        
class LoadoutUploadTest(StableTestMixin, TestCase):
    ssw_filename = 'TestOwens OW-1.ssw'
    mechs_path   = 'data/test-mechs/'
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
      , 'num_loadouts' : 3
    }

    def setUp(self):
        self.stable = self.createStable()

        self.stablemech = self.addMech(self.stable, mech_name='Owens', mech_code='OW-1', omni_loadout='C')
        self.stablemechweek = self.stablemech.get_mechweek()
        
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
    
