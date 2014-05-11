from copy import deepcopy

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django_genshi import loader

from solaris.utils import deepcopy_append
from solaris.stablemanager.views import StableView
from solaris.stablemanager.ledger.models import Ledger, LedgerItem
from solaris.stablemanager.utils import stable_required
from solaris.battlereport.models import BroadcastWeek

from .forms import LedgerItemForm

class StableLedgerView(StableView):
    submenu_selected = 'Ledger'
    
    styles_list = deepcopy_append(StableView.styles_list, ['/static/css/ledger.css'])
    
    def __init__(self, *args, **kwargs):
        self.template = loader.get_template('stablemanager/ledger_list.tmpl')
        super(StableLedgerView, self).__init__(*args, **kwargs)
        

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
    
    @stable_required(add_stable=True)
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
            
        return super(StableLedgerView,self).dispatch(request, stable=stable, week=week_model, ledger=ledger_model)
    
    def get(self, request, stable=None, week=None, ledger=None):
                
        ledger_items = []      
        
        for (code, description) in LedgerItem.item_types:
            ledger_items.append( {
                'code' : code
            ,   'description' : description
            ,   'entries' : ledger.entries.filter(type=code)
            ,   'form'    : LedgerItemForm( initial={ 'type' : code } )
        } )
            
        body = self.template.generate(
            stable_name = stable.stable_name
        ,   week = week.week_number
        ,   ledger_items = ledger_items
        ,   opening_balance = ledger.opening_balance
        ,   closing_balance = ledger.closing_balance()
        )
        return HttpResponse(self.in_layout(body, request))
    
    def post(self, request, stable=None, week=None, ledger=None):
        form_values = deepcopy(request.POST)
        form_values['ledger'] = ledger.id
        form_values['tied'] = False
        
        form = LedgerItemForm(form_values)
        if form.is_valid():
            form.save()
        
        return self.get(request, stable=stable, week=week, ledger=ledger)
        
