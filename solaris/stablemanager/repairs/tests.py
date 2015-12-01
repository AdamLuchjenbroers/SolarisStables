from django.test import TestCase

from django.contrib.auth.models import User
from solaris.warbook.models import House
from solaris.stablemanager.models import Stable, StableWeek
from solaris.campaign.models import Campaign 

from .models import RepairBill

class RepairBillTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='test-user', email='lotsa_mechs@nowhere.com', password='pass')
 
        stable_user = User.objects.get(username='test-user')
        self.house = House.objects.get(house='House Marik')
        self.campaign = Campaign.objects.get_current_campaign()

        self.stable = Stable.objects.create(stable_name='Test Stable'
                                           , owner = stable_user
                                           , house = self.house 
                                           , campaign= self.campaign)

        #self.bill = RepairBill.objects.create(stableweek = 

    def test_fail(self):
        self.assertEqual(True, False, 'Repair Bill Tests not written yet')
