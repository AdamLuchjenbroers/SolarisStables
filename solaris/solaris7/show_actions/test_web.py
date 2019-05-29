from django.test import TestCase, Client
from django.core.urlresolvers import reverse

import json

from solaris.stablemanager.tests import StableTestMixin

class ActionsRegularUserTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')

    def test_get_campaignlist(self):
        url = reverse('campaign_actions_now', kwargs={'campaign_url' : 's7test'})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200, 'Failed to retrieve action list page, HTTP %s' % response.status_code)

    def test_set_week_started(self):
        url = reverse('campaign_actions_start', kwargs={'week' : 1, 'campaign_url' : 's7test'})
        response = self.client.post(url, {'start_week' : True})

        self.assertEquals(response.status_code, 400, 'Request to start week for unauthorised user not rejected, HTTP %s' % response.status_code)


class ActionsAdminUserTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        
        self.client = Client()
        self.client.login(username='test-user', password='pass')

        self.stable.owner.is_superuser = True
        self.stable.owner.save()

    def test_get_campaignlist(self):
        url = reverse('campaign_actions_now', kwargs={'campaign_url' : 's7test'})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200, 'Failed to retrieve action list page, HTTP %s' % response.status_code)

    def test_set_week_started(self):
        url = reverse('campaign_actions_start', kwargs={'week' : 1, 'campaign_url' : 's7test'})
        response = self.client.post(url, {'start_week' : True})

        self.assertEquals(response.status_code, 200, 'Request to start week for authorised user failed, HTTP %s' % response.status_code)
