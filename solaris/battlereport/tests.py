from django.test import TestCase
from django.db.models import Count
from .models import BroadcastWeek, Zodiac
'''
Runs a suite of tests to confirm that the BroadcastWeek model correctly implements the following behavior
  * Generates a new Broadcast Week if Advance is called and there is no next week present
  * Returns the next week if advance() is called and there is already a next week
Additionally, confirm Zodiac sign has rotated correctly.
'''
class BroadcastWeekTests(TestCase):
    
    def setUp(self):
        z_black = Zodiac.object.create(sign='Black', rules='Test')
        z_white = Zodiac.object.create(sign='White', rules='Test', next=z_black)
        z_black.next = z_white
        
        self.week_now = BroadcastWeek.objects.create(week_number=2, sign=z_white)
        self.week_past = BroadcastWeek.objects.create(week_number=1, sign=z_black, next_week=self.week_now)
        
    def test_advanceCurrentWeek(self):
        new_week = self.week_now.advance()
        
        check_count = BroadcastWeek.objects.filter(week_number=3).count()
        
        self.assertEqual(new_week.week_number, 3, 'Unexpected Week Number: %i' % new_week.week_number)
        self.assertEqual(check_count, 1, 'Duplicate Weeks found in Database')
        self.assertEqual(new_week.sign.sign, 'Black', 'Incorrect Zodiac Sign: %s', new_week.sign.sign)
                
    def test_advanceOldWeek(self):
        new_week = self.week_past.advance()
        
        check_count = BroadcastWeek.objects.filter(week_number=2).count()
        
        self.assertEqual(new_week.week_number, 2, 'Unexpected Week Number: %i' % new_week.week_number)
        self.assertEqual(check_count, 1, 'Duplicate Weeks found in Database')
        self.assertEqual(new_week.sign.sign, 'White', 'Incorrect Zodiac Sign: %s', new_week.sign.sign)
        