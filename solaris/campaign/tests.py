from django.test import TestCase
from .models import BroadcastWeek
'''
Runs a suite of tests to confirm that the BroadcastWeek model correctly implements the following behavior
  * Generates a new Broadcast Week if Advance is called and there is no next week present
  * Returns the next week if advance() is called and there is already a next week
Additionally, confirm Zodiac sign has rotated correctly.
'''
class BroadcastWeekTests(TestCase):
    
    def setUp(self):
        self.week_past = BroadcastWeek.objects.get(week_number=1)
        # Manual setup, since we aren't testing advance()
        self.week_now = BroadcastWeek.objects.create(week_number=2, sign=self.week_past.sign.next, campaign=self.week_past.campaign)
        
        self.week_past.next_week = self.week_now
        self.week_past.save()
        
    def test_advanceCurrentWeek(self):
        new_week = self.week_now.advance()
        
        check_count = BroadcastWeek.objects.filter(week_number=3).count()
        
        self.assertEqual(new_week.week_number, 3, 'Unexpected Week Number: %i' % new_week.week_number)
        self.assertEqual(check_count, 1, 'Duplicate Weeks found in Database')
        # Week 1 is Rat: -> Ox -> Tiger
        self.assertEqual(new_week.sign.sign, 'Tiger', 'Incorrect Zodiac Sign: %s' % new_week.sign.sign)
                
    def test_advanceOldWeek(self):
        new_week = self.week_past.advance()
        
        check_count = BroadcastWeek.objects.filter(week_number=2).count()
        
        self.assertEqual(new_week.week_number, 2, 'Unexpected Week Number: %i' % new_week.week_number)
        self.assertEqual(check_count, 1, 'Duplicate Weeks found in Database')
        # Week 1 is Rat: -> Ox
        self.assertEqual(new_week.sign.sign, 'Ox', 'Incorrect Zodiac Sign: %s' % new_week.sign.sign)
        
