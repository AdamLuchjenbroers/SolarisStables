from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import json

from solaris.stablemanager.views import StableViewMixin
from solaris.stablemanager.ledger.models import LedgerItem
from solaris.stablemanager.mechs.models import StableMechWeek
from solaris.stablemanager.repairs.models import RepairBill, RepairBillLineItem
from solaris.warbook.equipment.models import Equipment

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
    
    def get_context_data(self, **kwargs):
        page_context = super(RepairBillMixin, self).get_context_data(**kwargs)
        
        page_context['mech'] = self.mech
        page_context['bill'] = self.bill
        page_context['stableweek'] = self.bill.stableweek.stableweek
        page_context['week_navigation'] = False       
        
        return page_context

class RepairBillView(RepairBillMixin, TemplateView):
    template_name = 'stablemanager/repair_bill.html'
        
    def get_context_data(self, **kwargs):
        page_context = super(RepairBillView, self).get_context_data(**kwargs)
        
        page_context['mech'] = self.mech
        page_context['crit_table'] = self.mech.all_locations()     
        page_context['detail_class'] = 'mech-repair'

        week_args = { 'week' : self.bill.stableweek.stableweek.week.week_number }
        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('stable_overview', kwargs=week_args)},
          {'title' : 'Finances', 'url' : reverse('stable_ledger', kwargs=week_args)},
#          {'title' : 'Training', 'url' : reverse('stable_training', kwargs=week_args)},
          {'title' : 'Mechs', 'url' : reverse('stable_mechs', kwargs=week_args)},   
          {'title' : 'Pilots', 'url' : reverse('stable_pilots', kwargs=week_args)},    
          {'title' : 'Actions', 'url' : reverse('stable_actions', kwargs=week_args)},      
        ]
        
        return page_context

class RepairBillLineView(RepairBillMixin, TemplateView):
    template_name = 'stablemanager/fragments/repair_lines.html'
         
       
class AjaxCritObjectView(RepairBillMixin, View):
    def post(self, request):        
        try:
            location = request.POST['location']
            slot = int(request.POST['slot'])
            critted = (request.POST['critted'].upper() == 'TRUE')
 
            result = self.bill.setCritical(location, slot, critted=critted)
            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 401)
            
class AjaxDamageLocationView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            location = request.POST['location']
            damage = int(request.POST['damage'])
            damage_type = request.POST['type']

            result = None        
            if damage_type == 'armour':
                result = self.bill.setArmourDamage(location, damage)
            elif damage_type == 'structure':
                result = self.bill.setStructureDamage(location, damage)
            else:
                return HttpResponse('Unrecognised type %s' % type, 400)

            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxDestroyLocationView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            location = request.POST['location']

            self.bill.destroyLocation(location)
            result = self.bill.locationState(location)

            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxSetAmmunitionTypeView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            line_id = int(request.POST['lineid'])
            ammo_id = request.POST['ammoid']

            line = get_object_or_404(RepairBillLineItem, id=line_id)
            if self.bill != line.bill: 
                return HttpResponse('Line item does not exist in current bill', 400)

            newammo = get_object_or_404(Equipment, id=ammo_id)
            if line.ammo_type.ammo_for != newammo.ammo_for:
                return HttpResponse('Invalid Ammunition Type for %s' % line.ammo_type.ammo_for.name, 400)

            line.ammo_type = newammo
            if line.is_critted() or line.count > newammo.ammo_size:
                line.count = newammo.ammo_size
            line.updateAmmoCost()    

            result = {
              'critted' : line.is_critted()
            , 'amount'  : line.count
            }

            line.save()
 
            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxSetAmmunitionCountView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            line_id = int(request.POST['lineid'])
            new_count = int(request.POST['count'])

            line = get_object_or_404(RepairBillLineItem, id=line_id)
            if self.bill != line.bill: 
                return HttpResponse('Line item does not exist in current bill', 400)

            line.count = min(new_count, line.ammo_type.ammo_size)
            line.updateAmmoCost()

            return HttpResponse(json.dumps(line.count))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxSetCoredView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            cored = (request.POST['cored'].upper() == 'TRUE')

            self.bill.cored = cored
            self.bill.save()

            return HttpResponse(json.dumps(self.bill.cored))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxSetFinalView(RepairBillMixin, View): 
    def post(self, request):        
        try:
            complete = (request.POST['final'].upper() == 'TRUE')

            if complete == True or self.bill.can_be_reopened():
                self.bill.complete = complete
                self.bill.save()

            if complete == True:
                self.bill.create_ledger_entry()
            else:
                self.bill.remove_ledger_entry()

            return HttpResponse(json.dumps(self.bill.complete))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)

class AjaxDeleteBillView(RepairBillMixin, View): 
    def post(self, request):
        week = self.bill.stableweek.stableweek.week.week_number      
        self.bill.delete()
        
        destination = reverse('stable_mechs', kwargs={'week' : week})
        return HttpResponse(json.dumps(destination))
