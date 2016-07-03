from copy import deepcopy
import json

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponse 
from django.db import models

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import StableWeek, LedgerItem

from .forms import LedgerItemForm, LedgerDeleteForm

class StableLedgerView(StableWeekMixin, TemplateView):
    submenu_selected = 'Finances'
    template_name = 'stablemanager/stable_ledger.tmpl'
    view_url_name = 'stable_ledger'
        
    def get_context_data(self, **kwargs):
        page_context = super(StableLedgerView,self).get_context_data(**kwargs)
        
        self.ledger = get_object_or_404(StableWeek, stable=self.stable, week=self.week)
        page_context['ledger'] = self.ledger
        
        page_context['ledger_groups'] = []    
        tab_index=1;
        
        for (code, description) in LedgerItem.item_types:
            entries = self.ledger.entries.filter(type=code)

            new_group = {
                'code' : code
            ,   'description' : description
            ,   'form'    : LedgerItemForm( initial={ 'type' : code })
            ,   'subtotal' : entries.aggregate(models.Sum('cost'))['cost__sum']
            }

            if new_group['subtotal'] == None:
                new_group['subtotal'] = 0
                       
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
        form_values = deepcopy(request.POST)
        form_values['ledger'] = self.stableweek.id
        form_values['tied'] = False
        
        try:
            instance = LedgerItem.objects.get(id=form_values['id'], ledger=self.stableweek)
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
   
class LedgerAjaxMixin(StableWeekMixin):
    def dispatch(self, request, week=None, entry_id=None, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect

        self.get_stableweek()

        entry_id = self.get_call_parameter(request, 'entry_id', entry_id)
        self.entry = get_object_or_404(LedgerItem, week=self.stableweek, id=entry_id)

        try: 
            super(LedgerAjaxMixin, self).dispath(request, *args, **kwargs)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

class AjaxUpdateLedgerCostForm(LedgerAjaxMixin):
    def post(self, request, *args, **kwargs):
       self.entry.cost = int(request.POST['cost'])
       self.entry.save()

       result = {'cost' : self.entry.cost}
       return HttpResponse(json.dumps(result)) 

class AjaxUpdateLedgerDescriptionForm(LedgerAjaxMixin):
    def post(self, request, *args, **kwargs):
       self.entry.description = request.POST['description']
       self.entry.save()

       result = {'description' : self.entry.description}
       return HttpResponse(json.dumps(result)) 
