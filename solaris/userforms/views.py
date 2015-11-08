# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from urlparse import urlparse
from django.views.generic import FormView, CreateView
from allauth.account.views import LoginView, SignupView

from solaris.views import SolarisViewMixin

class SolarisLoginView(SolarisViewMixin, LoginView):
    pass
    
class SolarisRegistrationView(SolarisViewMixin, SignupView):   
    pass
            
def logout_user(request):
    logout(request)
    return redirect('/')