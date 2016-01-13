from django.views.generic import FormView, ListView
from django.http import HttpResponse
from django.conf import settings

import json
import uuid

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import LedgerItem
from solaris.stablemanager.repairs.models import RepairBill

from . import forms, models

class InitialMechPurchaseView(StableViewMixin, FormView):
    # Looks like Formset stuff isn't in Django main yet, so we'll have to improvise
    template_name = 'stablemanager/initial_mechs.tmpl'
    form_class = forms.InitialMechsForm
    success_url = '/stable/initial-pilots'

    def form_valid(self, form):
        for mechform in form:
            models.StableMech.objects.create_mech( stable = self.stable
                                                 , purchased_as = mechform.design
                                                 , purchased_on = self.stable.get_stableweek()
                                                 , create_ledger = True
                                                 )
         
        return super(InitialMechPurchaseView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(InitialMechPurchaseView, self).get_context_data(**kwargs)
        
        context['submit'] = 'Purchase All'
        context['form_class'] = 'list initial-mechs'
        context['initial_balance'] = self.stable.get_stableweek().opening_balance
        
        return context

class StableMechsCommon(StableWeekMixin, ListView):
    model = models.StableMechWeek    

    def get_queryset(self):
        return self.stableweek.mechs.all().order_by('current_design__tonnage','current_design__mech_name', 'current_design__mech_code')

class StableMechsView(StableMechsCommon):
    submenu_selected = 'Mechs'
    template_name = 'stablemanager/stable_mechs.tmpl'
    view_url_name = 'stable_mechs'

    def get_context_data(self, **kwargs):
        context = super(StableMechsView, self).get_context_data(**kwargs)
        
        context['completed_bills'] = RepairBill.objects.filter(stableweek__stableweek=self.stableweek, complete=True).order_by('cored')
        context['purchase_form'] = forms.MechUploadOrPurchaseForm()
        
        return context

class StableMechsListPart(StableMechsCommon):
    template_name = 'stablemanager/fragments/mech_action_list.html'


class MechPurchaseFormView(StableWeekMixin, FormView):
    template_name = 'stablemanager/forms/add_mech_form.html'
    form_class = forms.MechUploadOrPurchaseForm

    def post(self, request, *args, **kwargs):
        if 'mech_ssw' in request.FILES:
            self.mech_temp_file = '%s%s' % (settings.SSW_UPLOAD_TEMP, uuid.uuid4())
            with open(self.mech_temp_file, 'wb+') as sswtemp:
                for chunk in request.FILES['mech_ssw'].chunks():
                    sswtemp.write(chunk)

        return super(MechPurchaseFormView, self).post(request, *args, **kwargs)

    def add_catalog_mech(self, form):
        models.StableMech.objects.create_mech( stable = self.stable
                                             , purchased_as = form.design
                                             , purchased_on = self.stableweek
                                             , create_ledger = form.cleaned_data['as_purchase']
                                             )

    def form_valid(self, form):
        result = { 'success' : True }
        if form.cleaned_data['mech_source'] == 'C':
            self.add_catalog_mech(form)
        elif form.cleaned_data['mech_source'] == 'U':
            print self.request.FILES['mech_ssw']
        else:
            result['success'] = False

        return HttpResponse(json.dumps(result))       

    def form_invalid(self, form):
        for error in form.errors:
            print error

        result = {
          'success' : False
        , 'non_field_errors'  : [error for error in form.non_field_errors()]
        }
        return HttpResponse(json.dumps(result))       
