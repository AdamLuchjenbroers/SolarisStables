from copy import deepcopy
import json
import csv

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponse 
from django.db import models

from django.template import Context, loader

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import StableWeek, LedgerItem
from solaris.stablemanager.ajax import StableWeekAjax

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
 
        page_context['add_url'] = reverse('stable_ledger_add', kwargs={'week' : self.ledger.week.week_number})            
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

class StableLedgerCSV(StableWeekMixin, View):
    def get(self, request, week=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"%s Ledger - Week %s.csv\"' % (self.stable.stable_name, week)

        headers = ['Group','Description','Cost']
        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()

        for row in self.stableweek.entries.all().order_by('type'):
            row={
              'Group'       : row.get_type_display()
            , 'Description' : row.description
            , 'Cost'        : row.cost 
            }
            writer.writerow(row)

        return response
   
class StableLedgerAjax(StableWeekAjax):
    def dispatch(self, request, week=None, entry_id=None, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect

        self.get_stableweek()

        entry_id = self.get_call_parameter(request, 'entry_id', entry_id)
        self.entry = get_object_or_404(LedgerItem, ledger=self.stableweek, id=entry_id)

        return super(StableLedgerAjax, self).dispatch(request, *args, **kwargs)

    def render_interest(self):
        context = Context({'lineitem' : self.stableweek.ledger_interest, 'new' : True})
        template = loader.get_template('stablemanager/fragments/ledger_item.html')
        return template.render(context)

class AjaxAddLedgerForm(StableWeekAjax):
    def post(self, request, *args, **kwargs):
        cost = int(request.POST['cost'])
        description = request.POST['description']
        group = request.POST['group']

        new_entry = self.stableweek.entries.create(type=group, cost=cost, description=description)

        context = Context({'lineitem' : new_entry, 'new' : True})
        template = loader.get_template('stablemanager/fragments/ledger_item.html')
        entry_html = template.render(context)

        result = {
          'cost' : new_entry.cost
        , 'description' : new_entry.description
        , 'group' : new_entry.type
        , 'entry_html' : entry_html
        }

        self.stableweek.recalculate()

        if self.stableweek.ledger_interest != None:
            context = Context({'lineitem' : self.stableweek.ledger_interest, 'new' : True})
            result['interest_html'] = template.render(context)

        return HttpResponse(json.dumps(result)) 

class AjaxUpdateLedgerCostForm(StableLedgerAjax):
    def post(self, request, *args, **kwargs):
        self.entry.cost = int(request.POST['cost'])
        self.entry.save()
        self.stableweek.recalculate()

        result = {'cost' : self.entry.cost}
        if self.stableweek.ledger_interest != None:
            result['interest_html'] = self.render_interest()

        return HttpResponse(json.dumps(result)) 

class AjaxUpdateLedgerDescriptionForm(StableLedgerAjax):
    def post(self, request, *args, **kwargs):
        self.entry.description = request.POST['description']
        self.entry.save()

        result = {'description' : self.entry.description}
        return HttpResponse(json.dumps(result))

class AjaxRemoveLedgerItem(StableLedgerAjax): 
    def post(self, request, *args, **kwargs):
        self.entry.delete()
        self.stableweek.recalculate()

        result = {'success' : True}
        if self.stableweek.ledger_interest != None:
            result['interest_html'] = self.render_interest()

        return HttpResponse(json.dumps(result))
