from django.test import TestCase
from decimal import Decimal

from solaris.utilities.loader import SSWLoader
from .models import MechDesign
from .refit import refit_cost


class RefitTestMixin(object):
    mechs_path   = 'data/test-mechs/'
    mechfile_spec = 'RefitTest %s.ssw'
    first_code = 'RFT-0'
    second_code = 'RFT-A'

    first_to_second = 0
    second_to_first = 0

    def setUp(self):
        mechfile = self.__class__.mechfile_spec % self.__class__.first_code
        self.first_loader = SSWLoader(mechfile, basepath=self.__class__.mechs_path)
        self.first_loader.load_mechs(print_message=False)
        self.first = MechDesign.objects.get(mech_name='RefitTest', mech_code=self.__class__.first_code, omni_loadout='Base')

        mechfile = self.__class__.mechfile_spec % self.__class__.second_code
        self.second_loader = SSWLoader(mechfile, basepath=self.__class__.mechs_path)
        self.second_loader.load_mechs(print_message=False)
        self.second = MechDesign.objects.get(mech_name='RefitTest', mech_code=self.__class__.second_code, omni_loadout='Base')

    def refit_check(self, oldcode, oldmech, newcode, newmech, expected):
        cost = refit_cost(oldmech, newmech)
        self.assertEqual(expected, cost, 'Refit from %s to %s should cost %.2f, got %.2f'
                         % (oldcode, newcode, expected, cost) ) 

    def test_firstToSecond(self):
        self.refit_check(self.__class__.first_code, self.first, self.__class__.second_code, self.second, self.__class__.first_to_second)

    def test_secondToFirst(self):
        self.refit_check(self.__class__.second_code, self.second, self.__class__.first_code, self.first, self.__class__.second_to_first)


class RefitTestBaseToArmour(RefitTestMixin, TestCase):
    first_code = 'RFT-0'
    second_code = 'RFT-A'

    # Adds 2 tons standard armour (20000) x 1.3 = 26000 CBilss
    first_to_second = 26000
    # Adds 2 Medium Lasers (2 x 40000) x 1.3 = 104000 CBills
    second_to_first = 104000

class RefitTestArmourToFerro(RefitTestMixin, TestCase):
    first_code = 'RFT-A'
    second_code = 'RFT-AF'

    # Replaces armour w/ 6 Tons FF and adds a small laser
    # (6 x 20000) + 11250 = 131250
    # 131250 x 1.3 = 170625
    first_to_second = 170625
    # Replaces armour w/  6.5 Tons of Standard Armour
    # (6.5 x 10000) x 1.3 = 84500
    second_to_first = 84500


class RefitTestBaseToEN(RefitTestMixin, TestCase):
    first_code = 'RFT-0'
    second_code = 'RFT-EN'

    # 180 Standard Engine     : (5000 x 30 x 180) / 75 = 360000   
    # .5 Tons Standard Armor  : 10000 x 0.5 = 5000
    # 365000 x 1.3 = 474500
    first_to_second = 474500

    # 150 Standard Engine      : (5000 x 30 x 150) / 75 = 300000   
    # 2 Medium Lasers          : 2 x 40000              =  80000
    # 1 Heatsink	       : 1 x 2000               =   2000
    #                                     i      Total:   382000 
    # 382000 x 1.3 = 496600
    second_to_first = 496600

class RefitTestBaseToXL(RefitTestMixin, TestCase):
    first_code = 'RFT-0'
    second_code = 'RFT-XL'

    # 210 XL Engine         : (20000 x 30 x 210) / 75 = 1680000
    # 3 Ton Standard Gyro   : 300000 x 3              =  900000 
    # 2 Tons Standard Armor : 2 x 10000               =   20000
    # 2600000 x 1.3 = 3380000
    first_to_second = 3380000

    # 150 Standard Engine      : (5000 x 30 x 150) / 75 = 300000   
    # 2 Ton Standard Gyro      : 300000 x 2             = 600000
    # 2 Medium Lasers          : 2 x 40000              =  80000
    # 2 Heatsinks	       : 2 x 2000               =   4000
    #                                            Total:   984000 
    # 984000 x 1.3 = 1279200
    second_to_first = 1279200

class RefitTesXLToXLG(RefitTestMixin, TestCase):
    first_code = 'RFT-XL'
    second_code = 'RFT-XLG'

    # 1.5 Ton XL Gyro : 750000 x 1.5 = 1125000
    # 1 Medium Laser                 =   40000
    # 1 Small Laser                  =   11250
    #                          Total : 1176250
    # 1176250 x 1.3 = 1529125
    first_to_second = 1529125
  
    # 3 Ton Standard Gyro   : 300000 x 3 = 900000
    # 900000 x 1.3 = 1170000
    second_to_first = 1170000 
