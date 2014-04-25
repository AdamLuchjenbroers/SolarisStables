"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client

class URLBasicTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_stableRedirect(self):
        response = self.client.get('/stable/')
        self.assertEqual(response.status_code, 302, 'Non-logged in users not redirected away from stable')
