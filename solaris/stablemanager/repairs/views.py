from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

import json

from solaris.stablemanager.views import StableViewMixin
from solaris.stablemanager.ledger.models import LedgerItem
from solaris.stablemanager.mechs.models import StableMechWeek
from solaris.stablemanager.repairs.models import RepairBill

class CreateRepairBillView(StableViewMixin, View):
    def get(self, request, stablemech=0):
        mech = get_object_or_404(StableMechWeek, id=stablemech)
        
        if mech.stableweek.stable != self.stable:
            return HttpResponse('Not your mech', 401)
        
        # Check if an incomplete bill already exists for this mech
        # before creating a new one.
        bill = mech.active_repair_bill()
        if bill == None:
            bill = RepairBill.objects.create(mech = mech.current_design, stableweek=mech)
            
        return HttpResponseRedirect(bill.get_absolute_url())

class RepairBillMixin(StableViewMixin):      
    def dispatch(self, request, bill=0, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect 
        
        self.bill = get_object_or_404(RepairBill, id=bill)         
        self.mech = self.bill.mech   
        
        if self.bill.stableweek.stableweek.stable != self.stable:
            return HttpResponse('Not your mech', 401)  
                   
        return super(RepairBillMixin, self).dispatch(request, *args, **kwargs)     

class RepairBillView(RepairBillMixin, TemplateView):
    template_name = 'stablemanager/repair_bill.html'
        
    def get_context_data(self, **kwargs):
        page_context = super(RepairBillView, self).get_context_data(**kwargs)
        
        page_context['mech'] = self.mech
        page_context['crit_table'] = self.mech.all_locations()     
        page_context['detail_class'] = 'mech-repair'
        
        return page_context
    
class AjaxCritObjectView(RepairBillMixin, View):
    def post(self, request):        
        try:
            location = request.POST['location']
            slot = int(request.POST['slot'])
            critted = request.POST['critted']
        
            result = self.bill.setCritical(location, slot, critted=critted)
            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 401)
            
        