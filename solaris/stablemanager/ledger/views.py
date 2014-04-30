from solaris.stablemanager.views import StableView
from genshi import Markup
from django.http import HttpResponse

#from django_genshi import loader

class StableLedgerView(StableView):
    
    def get(self, request, stable=None, week=None):
        body = Markup('<P>Stable Ledgers and Finance for the %s will go here</P><P>The Selected Broadcast Week is: %s</P>' % (stable.stable_name, week))
        return HttpResponse(self.in_layout(body, request))
        