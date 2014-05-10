from solaris.stablemanager.views import StableView
from genshi import Markup
from django.http import HttpResponse

#from django_genshi import loader

class StableTrainingView(StableView):
    submenu_selected = 'Training'
    
    def get(self, request, stable=None, week=None):
        body = Markup('<P>The Training Ledger for the %s will go here</P><P>The Selected Broadcast Week is: %s</P>' % (stable.stable_name, week))
        return HttpResponse(self.in_layout(body, request))
        