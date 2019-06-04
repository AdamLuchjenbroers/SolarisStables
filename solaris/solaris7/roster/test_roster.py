from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from solaris.stablemanager.tests import StableTestMixin

from . import models

from solaris.solaris7.fightinfo.models import Map, FightType, WeightClass

class TestAddFightByWeightClass(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.form = {
          'fight_type' : FightType.objects.first().id
        , 'fight_map' : Map.objects.first().id
        , 'purse' : 1500000
        , 'weightclass' : WeightClass.objects.first().id
        , 'week' : 1
	}

        self.submit_url = reverse('campaign_add_fights', kwargs={'week': 1, 'campaign_url': 's7test' }) 

        self.client = Client()
        self.client.login(username='test-user', password='pass')

        self.response = self.client.post(self.submit_url, self.form)

    def test_success_code(self):
        self.assertEqual(self.response.status_code, 201, 'Expected HTTP 201 on successful add, got HTTP %s' % self.response.status_code)
