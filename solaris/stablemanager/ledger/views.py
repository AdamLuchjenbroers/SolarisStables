from genshi import Markup
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
#from django_genshi import loader

from solaris.stablemanager.views import StableView
from solaris.stablemanager.ledger.models import Ledger, LedgerItem
from solaris.battlereport.models import BroadcastWeek

class StableLedgerView(StableView):
    submenu_selected = 'Ledger'

    def create_ledger(self, stable, week):
        return Ledger.objects.create(
            stable = stable
        ,   week = week        
        ,   opening_balance = 1000000
        )
        #TODO: Create the ledger, deriving opening balance from
        # previous entries if available (otherwise default to 10,000,000 credits
        # - the starting balance for a new stable).
        raise Http404
    
    def dispatch(self, request, stable=None, week=None):
        if week == None:
            week_model = stable.current_week
            current_week = True
        else:
            week_model = get_object_or_404(BroadcastWeek, week_number = week)
            current_week = False
            
        try:
            ledger_model = Ledger.objects.get(stable=stable, week=week_model)
        except Ledger.DoesNotExist:
            if current_week:
                self.create_ledger(stable, week_model)
            else:
                raise Http404
            
        super(StableLedgerView,self).dispatch(request, stable=stable, week=week_model, ledger=ledger_model)
    
    def get(self, request, stable=None, week=None, ledger=None):
                
        ledger_items = dict()       
        
        for (code, description) in LedgerItem.item_types:
            ledger_items[code] = dict()
            ledger_items[code]['description'] = description
            ledger_items[code]['items'] = ledger.entries.filter(type=code)
            ledger_items[code]['form'] = None #TODO
        
        body = Markup('<P>Stable Ledgers and Finance for the %s will go here</P><P>The Selected Broadcast Week is: %s</P>' % (stable.stable_name, week.week_number))
        return HttpResponse(self.in_layout(body, request))
