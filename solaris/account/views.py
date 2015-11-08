# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.views import LoginView, SignupView, ConfirmEmailView

from solaris.views import SolarisViewMixin

class SolarisLoginView(SolarisViewMixin, LoginView):
    pass
    
class SolarisRegistrationView(SolarisViewMixin, SignupView):   
    pass

class SolarisConfirmEmailView(SolarisViewMixin, ConfirmEmailView):
    pass
            
def logout_user(request):
    logout(request)
    return redirect('/')