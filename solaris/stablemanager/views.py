from genshi import Markup
from solaris.core import render_page
from solaris.stablemanager import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='/login')
def stable_main(request):
    
    stableList = models.Stable.objects.filter(owner = request.user)
    
    if len(stableList) <> 1:
        return redirect('/stable/register')
            
    stable = stableList[0]
            
    body = Markup('<P>Stable Management for the %s will go here</P>' % stable.stable_name )
    return render_page(body=body, selected=None, request=request)

@login_required(login_url='/login')
def stable_registration(request):
    body = Markup('<P>This will become a Stable Registration Page</P>')
    return render_page(body=body, selected=None, request=request)
