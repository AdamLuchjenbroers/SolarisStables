from django.test import TestCase, Client

from .models import Equipment

class MockMech():
    def __init__(self, tonnage=50, engine_rating=200):
        self.tonnage = tonnage
        self.engine_rating = engine_rating

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

    def test_standardTonnageFunc(self):
        self.assertEquals(self.standard.tonnage_func, 'armour', 'Structure equipment has incorrect tonnage function (%s)' % self.standard.tonnage_func) 
    def test_standardLow(self):
        tons = self.standard.tonnage(units=16)
        self.assertEquals(tons, 1, 'Expected 8 Units of Standard Structure = 1 Ton, got %2.1f Tons' % tons) 
    
    def test_standardRounding(self):
        tons = self.standard.tonnage(units=17)
        self.assertEquals(tons, 1.5, 'Expected 9 Units of Standard Structure to round up to 1.5 Tons, got %2.1f Tons' % tons) 

    def test_standardHigh(self):
        tons = self.standard.tonnage(units=56)
        self.assertEquals(tons, 3.5, 'Expected 56 Units of Standard Structure = 1 Ton, got %2.1f Tons' % tons) 

    def test_standardCostLow(self):
        cost = self.standard.cost(MockMech(), units=16)
        self.assertEquals(cost, 10000, 'Expected 1 Ton (16 Units) of armour to cost 10000, got %.2f' % cost)  

    def test_standardCostHigh(self):
        cost = self.standard.cost(MockMech(), units=56)
        self.assertEquals(cost, 35000, 'Expected 3.5 Tons (56 Units) of armour to cost 35000, got %.2f' % cost) 

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
