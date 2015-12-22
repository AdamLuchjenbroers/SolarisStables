from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

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

class RepairBillView(StableViewMixin, TemplateView):
    template_name = 'stablemanager/repair_bill.html'
    
    def get(self, request, bill):
        self.bill = get_object_or_404(RepairBill, id=bill)
        
        if self.bill.stableweek.stableweek.stable != self.stable:
            return HttpResponse('Not your mech', 401)
        else:
            self.mech = self.bill.mech
            return super(RepairBillView, self).get(request)
        
    def get_context_data(self, **kwargs):
        page_context = super(RepairBillView, self).get_context_data(**kwargs)
        
        page_context['mech'] = self.mech
        page_context['crit_table'] = self.mech.all_locations()     
        page_context['detail_class'] = 'mech-repair'
        
        return page_context