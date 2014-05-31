from django.test import TestCase
from .models import MechDesign

class MechMathsTest(TestCase):
    
    def setUp(self):
        MechDesign.objects.create(mech_name='Wolverine', mech_code='WVR-7D', tonnage=55, engine_rating=275, credit_value=11214457, bv_value=1314 )
        MechDesign.objects.create(mech_name='Raven', mech_code='RVN-4L', tonnage=35, engine_rating=210, credit_value=6001425, bv_value=873 )
        
    
    def test_walkingMP(self):
        """
        Tests that the engine 'size' formula is implemented correctly
        """
        wolverine = MechDesign.objects.get(mech_name='Wolverine', mech_code='WVR-7D')
        self.assertEqual(wolverine.move_walk(), 5,  'Failed Test: Testing Walking MP, expected 5, got %i' % wolverine.move_walk())
        
    
    def test_runningMP_Even(self):
        """
        Tests that running MP is calculated correctly
        """
        raven = MechDesign.objects.get(mech_name='Raven', mech_code='RVN-4L')
        self.assertEqual(raven.move_run(), 9, 'Failed Test: Testing Running MP Formula (even), expected 9, got %i' % raven.move_run())
        
    def test_runningMP_Odd(self):
        """
        Tests that running MP is calculated correctly
        """
        wolverine = MechDesign.objects.get(mech_name='Wolverine', mech_code='WVR-7D')
        self.assertEqual(wolverine.move_run(), 8, 'Failed Test: Running MP Formula (odd), expected 8, got %i' % wolverine.move_run())

