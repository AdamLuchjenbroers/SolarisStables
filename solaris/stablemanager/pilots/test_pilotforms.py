from django.test import TestCase, Client
from django.core.urlresolvers import reverse

import json

from solaris.stablemanager.tests import StableTestMixin

from solaris.warbook.models import House
from solaris.warbook.pilotskill.models import PilotRank, PilotTrait

from . import models

class PilotFormTestMixin(StableTestMixin):
    def setUp(self):
        self.stable = self.createStable()

        self.postdata = {
            'pilot-stable': self.stable.id
        ,   'pilot-pilot_callsign': 'Pinky'
        ,   'pilot-pilot_name': 'Test Eagle'
        ,   'pilot-affiliation': House.objects.get(house='House Davion').id
        ,   'pweek-rank' : PilotRank.objects.get(rank='Star').id
        ,   'pweek-skill_gunnery' : '4'
        ,   'pweek-skill_piloting' : '5'
        ,   'pweek-start_character_points' : '0'
        ,   'train-TOTAL_FORMS' : '2'
        ,   'train-INITIAL_FORMS' : '0'
        ,   'train-MIN_NUM_FORMS' : '0'
        ,   'train-MAX_NUM_FORMS' : '1000'
        ,   'train-0-trait' : PilotTrait.objects.get(name='Ammunition Pro', discipline__name='Missile').id
        ,   'train-0-notes' : ''
        ,   'train-1-trait' : PilotTrait.objects.get(name='Going down town').id
        ,   'train-1-notes' : 'King Missile'
        ,   'issue-TOTAL_FORMS' : '1'
        ,   'issue-INITIAL_FORMS' : '0'
        ,   'issue-MIN_NUM_FORMS' : '0'
        ,   'issue-MAX_NUM_FORMS' : '1000'
        ,   'issue-0-trait' : PilotTrait.objects.get(name='Ego Problem').id
        ,   'issue-0-notes' : ''
        }    

        self.client = Client()
        self.client.login(username='test-user', password='pass')

        self.add_url = reverse('stable_add_pilot', kwargs={'week' : 1})

    def fetch_pilot(self, callsign='Pinky'):
        return models.Pilot.objects.get(stable=self.stable, pilot_callsign=callsign)

    def fetch_pilotweek(self, week=1, callsign='Pinky'):
        sw = self.stable.get_stableweek(week)

        return sw.pilots.get(pilot__pilot_callsign=callsign)

    def test_add_pilot_record(self):
        response = self.client.post(self.add_url, self.postdata)
       
        qs = models.Pilot.objects.filter(pilot_callsign='Pinky')
        self.assertEqual(qs.count(), 1, 'Pilot form submitted, but pilot not found') 

    def test_add_pilot_record_pweek(self):
        response = self.client.post(self.add_url, self.postdata)
       
        qs = models.PilotWeek.objects.filter(pilot__pilot_callsign='Pinky', week__week__week_number=1)
        self.assertEqual(qs.count(), 1, 'Pilot form submitted, but pilot not found') 

class TestAddPilotForm(PilotFormTestMixin, TestCase):
    def test_add_pilot_response(self):
        response = self.client.post(self.add_url, self.postdata)

        self.assertEqual(response.status_code, 201, 'Form returned incorrect status code (HTTP %s)' % response.status_code)

    def test_check_name(self):
        response = self.client.post(self.add_url, self.postdata)
       
        pilot = self.fetch_pilot(callsign='Pinky')
        self.assertEqual(pilot.pilot_name, 'Test Eagle', 'Pilot created with incorrect name: Expected Test Eagle, got %s' % pilot.pilot_name)

    def test_count_traits(self):
        response = self.client.post(self.add_url, self.postdata)
        pw = self.fetch_pilotweek(callsign='Pinky')
        
        count = pw.traits.count() 
        self.assertEqual(count, 3, 'Expected 3 Traits, found %i' % count)

    def test_count_pilot_skills(self):
        response = self.client.post(self.add_url, self.postdata)
        pw = self.fetch_pilotweek(callsign='Pinky')
        
        count = pw.traits.filter(trait__discipline__discipline_type='T').count() 
        self.assertEqual(count, 2, 'Expected 2 Pilot Skills, found %i' % count)

    def test_count_pilot_issues(self):
        response = self.client.post(self.add_url, self.postdata)
        pw = self.fetch_pilotweek(callsign='Pinky')
        
        count = pw.traits.filter(trait__discipline__discipline_type='I').count() 
        self.assertEqual(count, 1, 'Expected 1 Pilot Issues, found %i' % count)


class TestEditPilotForm(PilotFormTestMixin, TestCase):
    def setUp(self):
        super(TestEditPilotForm, self).setUp()

        self.client.post(self.add_url, self.postdata)
        self.edit_url = reverse('stable_edit_pilot', kwargs={'week' : 1, 'callsign' : 'Pinky'})

    def test_change_name(self):
        self.postdata['pilot-pilot_name'] = 'Big Eagle'

        self.client.post(self.edit_url, self.postdata)
        pilot = self.fetch_pilot()
        
        self.assertEqual(pilot.pilot_name, 'Big Eagle', 'Pilot name change failed: Expected Big Eagle, got %s' % pilot.pilot_name)

    def test_change_callsign(self):
        self.postdata['pilot-pilot_callsign'] = 'Dipstick'

        self.client.post(self.edit_url, self.postdata)
        pilot = self.fetch_pilot(callsign='Dipstick')

        self.assertEqual(pilot.pilot_callsign, 'Dipstick', 'Pilot name change failed: Expected Big Eagle, got %s' % pilot.pilot_callsign)
        

    

   
