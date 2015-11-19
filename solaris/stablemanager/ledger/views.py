from copy import deepcopy

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import StableWeek, LedgerItem

from .forms import LedgerItemForm, LedgerDeleteForm

class StableLedgerView(StableWeekMixin, TemplateView):
    submenu_selected = 'Finances'
    template_name = 'stablemanager/stable_ledger.tmpl'
        
    def get_context_data(self, **kwargs):
        page_context = super(StableLedgerView,self).get_context_data(**kwargs)
        
        self.ledger = get_object_or_404(StableWeek, stable=self.stable, week=self.week)
        page_context['ledger'] = self.ledger
        
        page_context['ledger_groups'] = []    
        tab_index=1;
        
        for (code, description) in LedgerItem.item_types:
            new_group = {
                'code' : code
            ,   'description' : description
            ,   'form'    : LedgerItemForm( initial={ 'type' : code })
            }
                       
            entries = self.ledger.entries.filter(type=code)
            if entries:
                new_group['entries'] = []
                
                for item in entries:
                    form = LedgerItemForm(instance=item)
                    form.set_tabs(tab_index)
                    form.set_postURL( '/stable/ledger/%i' % self.week.week_number)
                    delete_form = LedgerDeleteForm(initial={
                                      'id' : item.id
                                    , 'week' : self.week.week_number
                                  })
                    tab_index += 1
                    new_group['entries'].append({
                        'item' : item
                    ,   'form' : form
                    ,   'delete' : delete_form
                    })
                    
            else:
                new_group['entries'] = None
                
            new_group['form'].set_tabs(tab_index)
            tab_index += 1          
                      
            page_context['ledger_groups'].append(new_group)
            
        page_context['opening_balance'] = self.ledger.opening_balance
        page_context['closing_balance'] = self.ledger.closing_balance()
            
        return page_context
    
    def post(self, request, stable=None, week=None, ledger=None):
        self.ledger = get_object_or_404(StableWeek, stable=self.stable, week=self.week)
        
        form_values = deepcopy(request.POST)
        form_values['ledger'] = self.ledger.id
        form_values['tied'] = False
                
        try:
            instance = LedgerItem.objects.get(id=form_values['id'], ledger=self.ledger)
        except (LedgerItem.DoesNotExist, KeyError, ValueError):
            instance = None
        
        form = LedgerItemForm(form_values, instance=instance)
        if form.is_valid():
            form.save()
        
        return self.get(request)
        
class StableLedgerDeleteView(StableViewMixin, View):
    def get(self, request):
        # Redirect back to main page
        return redirect(reverse('stable_ledger_now'))
        
    def post(self, request):
        try:
            item = LedgerItem.objects.get(id=request.POST['id'])
            
            # Check to make sure the deleted item belongs to the correct Stable
            if item.ledger.stable == self.stable:
                item.delete()
        except (LedgerItem.DoesNotExist, KeyError):
            pass
        
        return redirect('/stable/ledger')        
    
