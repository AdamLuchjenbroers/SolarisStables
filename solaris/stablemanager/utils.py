import urlparse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from .models import Stable

class stable_required(object):
    def __init__(self, login_url='/login', register_url='/stable/register', add_stable=False):
        self.login_url = login_url
        self.register_url = register_url
        self.add_stable = add_stable

    def __call__(self, function):
        func_self = self
        
        def decorator(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return redirect_to_login(
                                        request.get_full_path()
                                      , func_self.login_url
                                      , REDIRECT_FIELD_NAME
                                      )
                                        
        
            stableList = Stable.objects.filter(owner = request.user)
    
            if stableList.count() <> 1:
                return redirect(func_self.register_url)
        
            if self.add_stable:
                return function(request, *args, stable=stableList[0], **kwargs)
            else:
                return function(request, *args, **kwargs)   
            
        return decorator