from solaris.stablemanager.views import StableView
from solaris.stablemanager.ledger.models import Ledger, LedgerItem
from genshi import Markup
from django.http import HttpResponse, Http404
from django.core.exceptions import DoesNotExist

#from django_genshi import loader

class StableLedgerView(StableView):

    def create_ledger(self, stable, week):
        #TODO: Create the ledger, deriving opening balance from
        # previous entries if available (otherwise default to 10,000,000 credits
        # - the starting balance for a new stable).
        raise Http404
    
    def get(self, request, stable=None, week=None):
        if week == None:
            week = stable.current_week
            current_week = True
        else:
            current_week = False
            
        try:
            ledger = Ledger.objects.get(stable=stable, week=week)
        except DoesNotExist:
            if current_week:
                self.create_ledger(stable, week)
            else:
                raise Http404
               
        body = Markup('<P>Stable Ledgers and Finance for the %s will go here</P><P>The Selected Broadcast Week is: %s</P>' % (stable.stable_name, week))
        return HttpResponse(self.in_layout(body, request))
         