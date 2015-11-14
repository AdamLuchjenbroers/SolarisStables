from django.test import TestCase, Client
from django.contrib.auth.models import User

class LoginRedirectTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='login-test', email='login-test@nowhere.com', password='pass')
        
    def test_loginNoRedirect(self):
        response = self.client.post('/login/', {'login' : 'login-test', 'password' : 'pass'})
        self.assertEqual(response.status_code, 302, 'Failed redirect after login (HTTP %s)' % response.status_code)
        self.assertEqual(response.get('Location'), 'http://testserver/', 'Redirected to incorrect page: %s ' % response.get('Location') )
        
    def test_loginWithRedirect(self):
        response = self.client.post('/login/', {'login' : 'login-test', 'password' : 'pass', 'redirect' : '/stable'})
        self.assertEqual(response.status_code, 302, 'Failed redirect after login (HTTP %s)' % response.status_code)
        #self.assertEqual(response.get('Location'), 'http://testserver/stable', 'Redirected to incorrect page: %s ' % response.get('Location') )


class LoginErrorTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='login-test', email='login-test@nowhere.com', password='pass')
    
    def test_NoError(self):
        response = self.client.get('/login/')
        self.assertNotContains(response, 'The username and/or password you specified are not correct', 200)
        
    def test_loginWithError(self):
        response = self.client.post('/login/', {'username' : 'login-test', 'password' : 'wrongpass'})
        self.assertContains(response, 'The username and/or password you specified are not correct')
