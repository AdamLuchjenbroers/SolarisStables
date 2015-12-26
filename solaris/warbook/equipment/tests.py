from django.test import TestCase, Client, testcases

from .models import Equipment

class MockMech():
    def __init__(self, tonnage=50, engine_rating=200, jump=0):
        self.tonnage = tonnage
        self.engine_rating = engine_rating
        
    def jumping_mp(self):
        return jump

class ArmourTestCases(TestCase):
    def setUp(self):
        self.standard = Equipment.objects.get(ssw_name='Armour - Standard Armor')

    def test_standardTonnageFunc(self):
        self.assertEquals(self.standard.tonnage_func, 'armour', 'Armour equipment has incorrect tonnage function (%s)' % self.standard.tonnage_func) 

    def test_standardLow(self):
        tons = self.standard.tonnage(units=16)
        self.assertEquals(tons, 1, 'Expected 8 Units of Standard Armour = 1 Ton, got %2.1f Tons' % tons) 
    
    def test_standardRounding(self):
        tons = self.standard.tonnage(units=17)
        self.assertEquals(tons, 1.5, 'Expected 9 Units of Standard Armour to round up to 1.5 Tons, got %2.1f Tons' % tons) 

    def test_standardHigh(self):
        tons = self.standard.tonnage(units=56)
        self.assertEquals(tons, 3.5, 'Expected 56 Units of Standard Armour = 1 Ton, got %2.1f Tons' % tons) 

    def test_standardCostLow(self):
        cost = self.standard.cost(MockMech(), units=16)
        self.assertEquals(cost, 10000, 'Expected 1 Ton (16 Units) of armour to cost 10000, got %.2f' % cost)  

    def test_standardCostHigh(self):
        cost = self.standard.cost(MockMech(), units=56)
        self.assertEquals(cost, 35000, 'Expected 3.5 Tons (56 Units) of armour to cost 35000, got %.2f' % cost)  

class StructureTestCases(TestCase):
    def setUp(self):
        self.standard = Equipment.objects.get(ssw_name='Structure - Standard Structure')
        self.endo = Equipment.objects.get(ssw_name='Structure - Endo-Steel')

    def test_standardTonnageLow(self):
        tons = self.standard.tonnage(mech = MockMech(tonnage=35))
        self.assertEquals(tons, 3.5, 'Expected standard structure in a 35 ton mech to weigh 3.5 tons, got %.1f' % tons)

    def test_standardTonnageMed(self):
        tons = self.standard.tonnage(mech = MockMech(tonnage=55))
        self.assertEquals(tons, 5.5, 'Expected standard structure in a 55 ton mech to weigh 5.5 tons, got %.1f' % tons)

    def test_standardTonnageHigh(self):
        tons = self.standard.tonnage(mech = MockMech(tonnage=80))
        self.assertEquals(tons, 8.0, 'Expected standard structure in a 80 ton mech to weigh 8.0 tons, got %.1f' % tons)

    def test_standardTonnageFunc(self):
        self.assertEquals(self.standard.tonnage_func, 'structure', 'Structure equipment has incorrect tonnage function (%s)' % self.standard.tonnage_func) 

    def test_endoTonnageLow(self):
        tons = self.endo.tonnage(mech = MockMech(tonnage=35))
        self.assertEquals(tons, 2.0, 'Expected endo structure in a 35 ton mech to weigh 2.0 tons, got %.1f' % tons)

    def test_endoTonnageMed(self):
        tons = self.endo.tonnage(mech = MockMech(tonnage=55))
        self.assertEquals(tons, 3.0, 'Expected endo structure in a 55 ton mech to weigh 3.0 tons, got %.1f' % tons)

    def test_endoTonnageHigh(self):
        tons = self.endo.tonnage(mech = MockMech(tonnage=80))
        self.assertEquals(tons, 4.0, 'Expected endo structure in a 80 ton mech to weigh 4.0 tons, got %.1f' % tons)

    def test_endoTonnageFunc(self):
        self.assertEquals(self.endo.tonnage_func, 'structure', 'Structure equipment has incorrect tonnage function (%s)' % self.endo.tonnage_func) 

    def test_standardCostLow(self):
        cost = self.standard.cost(MockMech(), units=16)
        self.assertEquals(cost, 10000, 'Expected 16 structure units to cost 10000, got %.2f' % cost)  

    def test_standardCostHigh(self):
        cost = self.standard.cost(MockMech(), units=56)
        self.assertEquals(cost, 35000, 'Expected 56 structure units to cost 35000, got %.2f' % cost) 

class GyroTestCases(TestCase):
    def setUp(self):
        self.standard = Equipment.objects.get(ssw_name='Gyro - Standard Gyro')

    def gyroTonnageTest(self, gyro, engine_rating, expected):
        tons = self.standard.tonnage(mech = MockMech(engine_rating=engine_rating))
        self.assertEquals( tons, expected
                            , 'Expected Gyro for a %i engine to weigh %.1f tons, got %.1f tons' % (engine_rating, expected, tons) 
                            )

    def test_gyroTonnage150(self):
        self.gyroTonnageTest(self.standard, 150, 2)

    def test_gyroTonnage200(self):
        self.gyroTonnageTest(self.standard, 200, 2)

    def test_gyroTonnage201(self):
        self.gyroTonnageTest(self.standard, 201, 3)

class JumpjetTestCases(TestCase):
    def setUp(self):
        self.standard = Equipment.objects.get(ssw_name='Jumpjet - Standard Jump Jet')

    def jumpjetTonnageTest(self, mech_tons, expect_tons):
        actual_tons = self.standard.tonnage(mech=MockMech(tonnage=mech_tons))
        self.assertEquals( actual_tons, expect_tons
                            , 'Expected jumpjets on a %i ton mech to weigh %.1f tons, got %.1f' 
                            % (mech_tons, expect_tons, actual_tons)) 
       

    def test_jumpjetTons55(self):
        self.jumpjetTonnageTest(55, 0.5)

    def test_jumpjetTons60(self):
        self.jumpjetTonnageTest(60, 1.0)

    def test_jumpjetTons85(self):
        self.jumpjetTonnageTest(85, 1.0)

    def test_jumpjetTons90(self):
        self.jumpjetTonnageTest(90, 2.0)

class AESTestCases(TestCase):
    def setUp(self):
        self.aes = Equipment.objects.get(ssw_name='AES - Arm AES')

    def aesTonnageTest(self, mech_tons, expect_tons):
        actual_tons = self.aes.tonnage(mech=MockMech(tonnage=mech_tons))
        self.assertEquals( actual_tons, expect_tons
                         , 'Expected AES on a %i ton mech to weigh %.1f tons, got %.1f' 
                         % (mech_tons, expect_tons, actual_tons)) 

    def aesCriticalsTest(self, mech_tons, expect_crits):
        actual_crits = self.aes.criticals(mech=MockMech(tonnage=mech_tons))
        self.assertEquals( actual_crits, expect_crits
                         , 'Expected AES on a %i ton mech to require %i crits, got %i' 
                         % (mech_tons, expect_crits, actual_crits)) 

    def test_aesTons35(self):
        self.aesTonnageTest(35, 1.0)

    def test_aesTons40(self):
        self.aesTonnageTest(40, 1.5)

    def test_aesTons80(self):
        self.aesTonnageTest(80, 2.5)

    def test_aesCrits30(self):
        self.aesCriticalsTest(30, 1)

    def test_aesCrits40(self):
        self.aesCriticalsTest(40, 2)

    def test_aesCrits55(self):
        self.aesCriticalsTest(55, 2)

    def test_aesCrits60(self):
        self.aesCriticalsTest(60, 3)

    def test_aesCrits75(self):
        self.aesCriticalsTest(75, 3)

    def test_aesCrits80(self):
        self.aesCriticalsTest(80, 4)

    def test_aesCrits100(self):
        self.aesCriticalsTest(100, 4)
