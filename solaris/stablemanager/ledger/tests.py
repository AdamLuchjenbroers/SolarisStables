from django.test import TestCase

from solaris.battlereport.models import Zodiac, BroadcastWeek
from .models import Ledger, LedgerItem


class LedgerTests(TestCase):
    
    def setUp(self):
            
        z_black = Zodiac.object.create(sign='Black', rules='Test')
        z_white = Zodiac.object.create(sign='White', rules='Test', next=z_black)
        z_black.next = z_white
        
        self.week_now = BroadcastWeek.objects.create(week_number=2, sign=z_white)
        self.week_past = BroadcastWeek.objects.create(week_number=1, sign=z_black, next_week=self.week_now)
        
        #self.ledger = Ledger.objects.create()
        
    def test_computeClosingBalance(self):
        pass