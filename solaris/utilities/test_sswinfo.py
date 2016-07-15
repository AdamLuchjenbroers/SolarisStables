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

    def test_techbase(self):
        self.compare_by_key('techbase', 'Incorrect Technology Base: expected %s, got %s')     

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
      , 'techbase'  : 'Inner Sphere' 
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
      , 'techbase'  : 'Inner Sphere' 
    }

    def test_configA_exists(self):
        self.assertIn('A', self.info['loadouts'], 'Config A not found')

    def test_configA_cost(self):
        cost = self.info['loadouts']['A']['cost']
        expect = 3274781.25
        self.assertEqual(cost, expect, 'Cost for config A is %s, expected %s' % (cost, expect))

    def test_configA_bv(self):
        cost = self.info['loadouts']['A']['bv']
        expect = 814
        self.assertEqual(cost, expect, 'Battle Value for config A is %s, expected %s' % (cost, expect))

    def test_configB_exists(self):
        self.assertIn('B', self.info['loadouts'], 'Config B not found')

    def test_configB_cost(self):
        cost = self.info['loadouts']['B']['cost']
        expect = 3110250
        self.assertEqual(cost, expect, 'Cost for config B is %s, expected %s' % (cost, expect))

    def test_configB_bv(self):
        cost = self.info['loadouts']['B']['bv']
        expect = 700
        self.assertEqual(cost, expect, 'Battle Value for config B is %s, expected %s' % (cost, expect))

    def test_configC_exists(self):
        self.assertIn('C', self.info['loadouts'], 'Config C not found')

    def test_configC_cost(self):
        cost = self.info['loadouts']['C']['cost']
        expect = 3049312.5
        self.assertEqual(cost, expect, 'Cost for config C is %s, expected %s' % (cost, expect))

    def test_configC_bv(self):
        cost = self.info['loadouts']['C']['bv']
        expect = 747
        self.assertEqual(cost, expect, 'Battle Value for config C is %s, expected %s' % (cost, expect))
