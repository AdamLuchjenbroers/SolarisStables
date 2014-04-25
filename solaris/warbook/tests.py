"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client

class URLBasicTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_techtreeURL(self):
        response = self.client.get('/reference/techtree/')
        self.assertEqual(response.status_code, 200, 'Unable to retrieve tech-tree list')      
    
    def test_pilotskillURL(self):
        response = self.client.get('/reference/pilotskills/')
        self.assertEqual(response.status_code, 200, 'Unable to retrieve pilot-skill list')
        

