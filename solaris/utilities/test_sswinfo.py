from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from solaris.utilities.loader import SSWLoader

class SSWLoaderTestMixin(object):
    ssw_filename = 'TestMech.ssw'
    mechs_path   = 'data/test-mechs/'

    expect = {}

    def setUp(self):
        self.loader = SSWLoader(self.__class__.ssw_filename, basepath=self.__class__.mechs_path)

        self.info = self.loader.get_model_details()
        self.expect = self.__class__.expect

        super(SSWLoaderTestMixin, self).setUp()

    def compare_by_key(self, key, errorstring):
        self.assertEqual(self.expect[key], self.info[key], errorstring % (self.expect[key], self.info[key]))

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

class BasicSSWTests(SSWLoaderTestMixin, TestCase):
    ssw_filename = 'SimpleLoadingTest SLT-1.ssw'
    expect = {
        'mech_name' : 'SimpleLoadingTest' 
      , 'mech_code' : 'SLT-1'
      , 'is_omni'   : False
      , 'tons'      : 50
      , 'bv'        : 1167 
      , 'cost'      : 4029500 
      , 'motive_type' : 'Biped'
    }

class OmniSSWTests(SSWLoaderTestMixin, TestCase):
    ssw_filename = 'OmniLoadingTest OLT-1.ssw'
    expect = {
        'mech_name' : 'OmniLoadingTest' 
      , 'mech_code' : 'OLT-1'
      , 'is_omni'   : True
      , 'tons'      : 30
      , 'bv'        : None 
      , 'cost'      : 3049312.5
      , 'motive_type' : 'Biped'
    }
