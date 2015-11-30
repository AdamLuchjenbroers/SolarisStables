from django.test import TestCase, Client
from django.contrib.auth.models import User
from solaris.warbook.models import House
from solaris.stablemanager.models import Stable, StableWeek
from solaris.campaign.models import BroadcastWeek, Zodiac, Campaign

'''
Runs a suite of tests to confirm the main stable page handles the following three cases correctly:
 * Accessed by someone who isn't loggged in -> Redirect to login page
 * Accessed by an authenticated user who doesn't have a stable -> Redirect to stable registration page
 * Accessed by an authenticated user who has a stable -> Do not redirect
'''
class StableLoginTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='no-stable', email='has-no-stable@nowhere.com', password='pass')
        User.objects.create_user(username='has-stable', email='lotsa_mechs@nowhere.com', password='pass')
 
        stable_user = User.objects.get(username='has-stable')
        Stable.objects.create(stable_name='Test Stable'
                             , owner=stable_user
                             , house = House.objects.get(house='House Marik')
                             , campaign=Campaign.objects.get_current_campaign())
 

    def test_redirectNotLoggedIn(self):
        response = self.client.get('/stable/')
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from stable (HTTP %s)' % response.status_code)
        self.assertEqual(response.get('Location'), 'http://testserver/login?next=/stable/', 'Redirected to incorrect page: %s ' % response.get('Location') )
    
    def test_redirectNoStable(self):
        self.client.login(username='no-stable', password='pass')
        response = self.client.get('/stable/')
        
        self.assertEqual(response.status_code, 302, 'Users without a stable not redirected to stable registration page (HTTP %s)' % response.status_code)
        self.assertEqual(response.get('Location'), 'http://testserver/stable/register', 'Redirected to incorrect page: %s ' % response.get('Location') )
        
        self.client.logout()
        
    
    def test_clientHasStable(self):
        self.client.login(username='has-stable', password='pass')
        response = self.client.get('/stable/')
        
        self.assertEqual(response.status_code, 200, 'Page not rendered for user with a stable (HTTP %s)' % response.status_code)
        
        self.client.logout()


class StableSetupTests(TestCase):

    def setUp(self): 
        User.objects.create_user(username='has-stable', email='lotsa_mechs@nowhere.com', password='pass')
 
        stable_user = User.objects.get(username='has-stable')
        self.house = House.objects.get(house='House Marik')
        self.campaign = Campaign.objects.get_current_campaign()

        self.stable = Stable.objects.create(stable_name='Test Stable'
                                           , owner = stable_user
                                           , house = self.house 
                                           , campaign= self.campaign)

    def test_hasweek(self):
        week = self.stable.get_stableweek()
        self.assertIsInstance(week, StableWeek, 'Initial Stableweek missing')


    def test_initialbalance(self):
        week = self.stable.get_stableweek()
        self.assertEqual( week.opening_balance, self.campaign.initial_balance
                           , 'Iniiial balance set incorrectly, found %i, expected %i'
                           % (week.opening_balance, self.campaign.initial_balance) )

    def test_templates(self):
        for template in self.campaign.initial_pilots.all():
            pilotcount = self.stable.get_stableweek().pilots.filter( rank = template.rank
                                                                   , skill_gunnery = template.gunnery
                                                                   , skill_piloting = template.piloting ).count()
            self.assertEqual(pilotcount, template.count, 'Expected %i %s, found %i' % (template.count, template.rank.rank, pilotcount) ) 
