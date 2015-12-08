from django.test import TestCase
from .models import MechDesign

class MechMathsTest(TestCase):
    
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
        self.assertEqual(raven.move_walk(), 6, 'Failed Test: Expected walking MP of 6, got %i' % raven.move_walk())
        self.assertEqual(raven.move_run(), 9, 'Failed Test: Testing Running MP Formula (even), expected 9, got %i' % raven.move_run())
        
    def test_runningMP_Odd(self):
        """
        Tests that running MP is calculated correctly
        """
        wolverine = MechDesign.objects.get(mech_name='Wolverine', mech_code='WVR-7D')
        self.assertEqual(wolverine.move_run(), 8, 'Failed Test: Running MP Formula (odd), expected 8, got %i' % wolverine.move_run())

    def test_itemAt_Cockpit(self):
        """
        Tests that item_at returns the correct equipment object when used to retrieve the cockpit.
        """
        wolverine = MechDesign.objects.get(mech_name='Wolverine', mech_code='WVR-7D')
        cockpit = wolverine.item_at('HD', 3)
        self.assertEqual(cockpit.equipment.ssw_name, 'Cockpit - Standard Cockpit', 'Expected Cockpit in HD slot 3, found %s' % cockpit.equipment.ssw_name)

    def test_itemAt_Gyro(self):
        """
        Tests that item_at returns the correct equipment object when used to retrieve the gyro.
        """
        wolverine = MechDesign.objects.get(mech_name='Wolverine', mech_code='WVR-7D')
        gyro = wolverine.item_at('CT', 5)
        self.assertEqual(gyro.equipment.ssw_name, 'Gyro - Standard Gyro', 'Expected Cockpit in HD slot 3, found %s' % gyro.equipment.ssw_name)
