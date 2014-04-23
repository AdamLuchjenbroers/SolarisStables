from django.test import TestCase
from .models import MechDesign

class MechMathsTest(TestCase):
    test_mech = MechDesign()
    
    def setUp(self):
        self.test_mech
        self.test_mech.tonnage = 40
        self.test_mech.move_walk = 4
        
    
    def test_enginerating(self):
        """
        Tests that the engine 'size' formula is implemented correctly
        """
        self.assertEqual(self.test_mech.engine_rating(), 160, 'Testing engine rating formula')
        
    
    def test_runningMP_Even(self):
        """
        Tests that running MP is calculated correctly
        """
        self.assertEqual(self.test_mech.move_run(), 6, 'Testing Running MP Formula (even)')
        
    def test_runningMP_Odd(self):
        """
        Tests that running MP is calculated correctly
        """
        self.test_mech.move_walk = 3
        self.assertEqual(self.test_mech.move_run(), 5, 'Testing Running MP Formula (odd)')
        self.test_mech.move_walk = 4

