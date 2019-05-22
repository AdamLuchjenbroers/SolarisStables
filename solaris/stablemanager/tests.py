from django.test import TestCase, Client
from django.contrib.auth.models import User

from solaris.warbook.models import House
from solaris.warbook.mech.models import MechDesign
from solaris.warbook.pilotskill import models as pilotskill_models

from solaris.campaign.models import Campaign
from solaris.campaign.solaris7.models import BroadcastWeek, Zodiac, SolarisCampaign

from solaris.stablemanager.models import Stable, StableWeek
from solaris.stablemanager.mechs.models import StableMech, StableMechWeek
from solaris.stablemanager.pilots import models as pilot_models

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
                           , 'Initial balance set incorrectly, found %i, expected %i'
                           % (week.opening_balance, self.campaign.initial_balance) )

    def test_templates(self):
        for template in self.campaign.initial_pilots.all():
            pilotcount = self.stable.get_stableweek().pilots.filter( rank = template.rank
                                                                   , skill_gunnery = template.gunnery
                                                                   , skill_piloting = template.piloting ).count()
            self.assertEqual(pilotcount, template.count, 'Expected %i %s, found %i' % (template.count, template.rank.rank, pilotcount) )

class StableTestMixin(object):
    def createStable(self, userName='test-user', stableName='Test Stable'):
        User.objects.create_user(username=userName, email='lotsa_mechs@nowhere.com', password='pass')
 
        stable_user = User.objects.get(username=userName)
        stable = Stable.objects.create(stable_name=stableName
                             , owner=stable_user
                             , house = House.objects.get(house='House Marik')
                             , campaign=Campaign.objects.get_current_campaign())

        return stable

    def advanceWeek(self, stable): 
        sw = stable.get_stableweek()
        sw.week.advance()
        return sw.advance()

    def addMech(self, stable, stableweek=None, create_ledger=True, **kwargs):
        if stableweek == None:
            stableweek = stable.get_stableweek()

        mechdesign = MechDesign.objects.get(**kwargs)
        mech = StableMech.objects.create_mech( stable = stable
                                             , purchased_as = mechdesign
                                             , purchased_on = stableweek
                                             , create_ledger = create_ledger
                                             )
        return mech

    def add_pilot(self, stable, stableweek=None, **kwargs):
        if stableweek == None:
            stableweek = stable.get_stableweek()

        pilot_args = {
          'pilot_name' : kwargs.get('pilot_name', 'Tess Teagle')
        , 'pilot_callsign' : kwargs.get('pilot_callsign', 'Test')
        , 'affiliation' : kwargs.get('affiliation', stable.house)
        , 'stable' : stable
        }
        pilot = pilot_models.Pilot.objects.create(**pilot_args)

        pweek_args = {
          'pilot' : pilot
        , 'week' : stableweek
        , 'skill_gunnery' : kwargs.get('skill_gunnery', 4)
        , 'skill_piloting' : kwargs.get('skill_piloting', 5)
        , 'rank' : kwargs.get('rank', pilotskill_models.PilotRank.objects.get(rank='Rookie'))
        , 'wounds' : kwargs.get('wounds', 0)
        }

        pilotweek = pilot_models.PilotWeek.objects.create(**pweek_args)

        return (pilot, pilotweek)

class StableWeekTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.campaign = self.stable.campaign
        self.campaign.current_week().advance()

    def test_advance_returns(self):
        sw = self.stable.get_stableweek()

        next_sw = sw.advance()
        self.assertIsInstance(next_sw, StableWeek, 'Advancing Stableweek did not return a stableweek, instead returned %s' % next_sw)

    def test_advance_nextweek(self):
        sw = self.stable.get_stableweek()

        next_sw = sw.advance()
        self.assertEquals(next_sw.week.week_number, 2, 'Advancing Stableweek did not return Week 2, instead returned %s' % next_sw)

    def test_advance_linkage(self):
        sw = self.stable.get_stableweek()

        next_sw = sw.advance()
        self.assertEquals(sw.next_week, next_sw, 'Linkage missing betweek stable weeks, next_week currently set to %s' % sw.next_week)

    def test_advance_reverse_linkage(self):
        sw = self.stable.get_stableweek()

        next_sw = sw.advance()
        self.assertEquals(sw, next_sw.prev_week, 'Reverse linkage missing betweek stable weeks, prev_week currently set to %s' % next_sw.prev_week)
