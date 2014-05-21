from copy import deepcopy

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django_genshi import loader

from solaris.utils import deepcopy_append
from solaris.stablemanager.views import StableView
from solaris.stablemanager.ledger.models import Ledger, LedgerItem
from solaris.stablemanager.utils import stable_required
from solaris.battlereport.models import BroadcastWeek

from .forms import LedgerItemForm, LedgerDeleteForm

class StableLedgerView(StableView):
    submenu_selected = 'Ledger'
    
    styles_list = deepcopy_append(StableView.styles_list, ['/static/css/ledger.css'])
    scripts_list = ['/static/js/jquery-1.11.1.js', '/static/js/stable_ledger.js']
    
    def __init__(self, *args, **kwargs):
        self.template = loader.get_template('stablemanager/ledger_list.genshi')
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
        tab_index=1;
        
        for (code, description) in LedgerItem.item_types:
            new_item = {
                'code' : code
            ,   'description' : description
            ,   'form'    : LedgerItemForm( initial={ 'type' : code })
            }
                       
            entries = ledger.entries.filter(type=code)
            if entries:
                new_item['entries'] = []
                
                for item in entries:
                    form = LedgerItemForm(instance=item)
                    form.set_tabs(tab_index)
                    form.set_postURL( '/stable/ledger/%i' % week.week_number)
                    delete_form = LedgerDeleteForm(initial={
                                      'id' : item.id
                                    , 'week' : week.week_number
                                  })
                    tab_index += 1
                    new_item['entries'].append({
                        'item' : item
                    ,   'form' : form
                    ,   'delete' : delete_form
                    })
                    
            else:
                new_item['entries'] = None
                
            new_item['form'].set_tabs(tab_index)
            tab_index += 1
                    
            ledger_items.append(new_item)

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
        
        try:
            instance = LedgerItem.objects.get(id=form_values['id'], ledger=ledger)
        except (LedgerItem.DoesNotExist, KeyError):
            instance = None
        
        form = LedgerItemForm(form_values, instance=instance)
        if form.is_valid():
            form.save()
        
        return self.get(request, stable=stable, week=week, ledger=ledger)
        
class StableLedgerDeleteView(StableView):
    def get(self, request, stable=None, week=None, ledger=None):
        # Redirect back to main page
        return redirect('/stable/ledger')
        
    def post(self, request, stable=None):
        try:
            item = LedgerItem.objects.get(id=request.POST['id'])
            
            # Check to make sure the deleted item belongs to the correct Stable
            if item.ledger.stable == stable:
                item.delete()
        except (LedgerItem.DoesNotExist, KeyError):
            pass
        
        return redirect('/stable/ledger')        
    