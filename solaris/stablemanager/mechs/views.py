from django.views.generic import View, TemplateView, FormView, ListView, UpdateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

import json
import uuid

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import LedgerItem
from solaris.stablemanager.repairs.models import RepairBill
from solaris.utilities.loader import SSWLoader
from solaris.files.views import CreateTempMechView

from . import forms, models
import sys

class PurchaseUploadMechView(CreateTempMechView):
    form_url_name = 'upload_purchase_mech'
    
    def form_valid(self, form):
        form.save()
        try:
            form.instance.load_from_file()

            result = form.instance.to_dict(loadout_filters={'design_status': 'N'})
            
            error_msg = None
            
            if result['design_status'] != 'N' and not result['is_omni']:
                error_msg = '%s %s already exists in database' % (result['mech_name'], result['mech_code'])
            elif result['is_omni'] and result['num_loadouts'] < 1:
                error_msg = 'No new configs for %s %s found in supplied file' % (result['mech_name'], result['mech_code'])
            
            if error_msg != None:
                result = {
                  'success' : False
                , 'errors'  : { 'SSW Data' : [error_msg] }
                }
                form.instance.delete()
                return HttpResponse(json.dumps(result), status=400) 
            else:      
                return HttpResponse(json.dumps(result))  
        except BaseException as e: 
            result = {
             'success' : False
            , 'errors'  : { 'SSW Data' : ['Failed to Parse Supplied File'] }
            }
            if settings.DEBUG:
                result['exception'] = e.message
            
            form.instance.delete()
            return HttpResponse(json.dumps(result), status=400)          

class InitialMechPurchaseView(StableViewMixin, FormView):
    # Looks like Formset stuff isn't in Django main yet, so we'll have to improvise
    template_name = 'stablemanager/initial_mechs.tmpl'
    form_class = forms.InitialMechsForm
    success_url = '/stable/initial-pilots'

    def form_valid(self, form):
        for mechform in form:
            if mechform.design == None:
                continue

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
        return self.stableweek.mechs.filter(config_for=None).order_by('current_design__tonnage','current_design__mech_name', 'current_design__mech_code')

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

    def form_valid(self, form):
        if form.cleaned_data['mech_source'] == 'U':
            self.stableweek.add_custom_design(form.design) 

        models.StableMech.objects.create_mech( stable = self.stable
                                             , purchased_as = form.design
                                             , purchased_on = self.stableweek
                                             , create_ledger = form.cleaned_data['as_purchase']
                                             , delivery = form.cleaned_data['delivery'] 
                                             )
        result = { 'success' : True }
        return HttpResponse(json.dumps(result))       

    def form_invalid(self, form):
        result = {
          'success' : False
        , 'errors'  : { field : error for (field, error) in form.errors.items() }
        }

        return HttpResponse(json.dumps(result), status=400)     

class MechModifyMixin(StableViewMixin):
    def dispatch(self, request, smw_id=0, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect

        self.stablemechweek = get_object_or_404(models.StableMechWeek, id=smw_id)
        self.stablemech = self.stablemechweek.stablemech

        self.stableweek = self.stablemechweek.stableweek
        if self.stableweek.stable != self.stable:
            return HttpResponse('Not your mech!', 401)

        return super(MechModifyMixin, self).dispatch(request, *args, **kwargs) 

    def get_object(self, queryset=None):
        return self.stablemechweek

    def get_form(self, form_class):
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

class RefitUploadMechView(CreateTempMechView):
    def form_valid(self, form):
        form.save()
        try:
            form.instance.load_from_file()

            result = form.instance.to_dict(loadout_filters={'design_status': 'N'})
            
            error_list = []
            current_chassis = self.stablemechweek.current_design.mech_name
            current_tonnage = self.stablemechweek.current_design.tonnage

            if result['is_omni']:
                error_list.append('Uploaded config is an Omnimech, not permitted for refits')

            if result['design_status'] != 'N':
                error_list.append('%s %s already exists in database' % (result['mech_name'], result['mech_code']))

            if result['mech_name'] != current_chassis:
                error_list.append('Uploaded load-out is for a %s, expected a %s' % (result['mech_name'], current_chassis))

            if result['tons'] != current_tonnage:
                error_list.append('Uploaded mech is %d tons, %s should be %d tons.' 
                                 % (result['tons'], current_chassis, current_tonnage))
            
            if len(error_list) > 0:
                result = {
                  'success' : False
                , 'errors'  : { 'SSW Data' : error_list }
                }
                return HttpResponse(json.dumps(result), status=400) 
            else:      
                return HttpResponse(json.dumps(result))  
        except BaseException as e: 
            result = {
             'success' : False
            , 'errors'  : { 'SSW Data' : ['Failed to Parse Supplied File'] }
            }
            if settings.DEBUG:
                result['exception'] = e.message
            
            return HttpResponse(json.dumps(result), status=400) 

    def dispatch(self, request, smw_id=0, *args, **kwargs):
        self.stablemechweek = get_object_or_404(models.StableMechWeek, id=smw_id)
        return super(RefitUploadMechView, self).dispatch(request, *args, **kwargs)


class OmniUploadMechView(CreateTempMechView):
    def form_valid(self, form):
        form.save()
        try:
            form.instance.load_from_file()

            result = form.instance.to_dict(loadout_filters={'design_status': 'N'})
            
            error_list = []
            current_chassis = self.stablemechweek.current_design.mech_name
            current_model   = self.stablemechweek.current_design.mech_code
            current_tonnage = self.stablemechweek.current_design.tonnage

            if not result['is_omni']:
                error_list.append('Uploaded config must be an Omnimech.')
            elif result['num_loadouts'] < 1:
                error_list.append('All supplied loadouts for %s %s already exist in database'
                                  % (result['mech_name'], result['mech_code']))

            if result['mech_name'] != current_chassis or result['mech_code'] != current_model:
                error_list.append('Uploaded load-out is for a %s %s, expected a %s %s.' 
                                 % (result['mech_name'], result['mech_code'], current_chassis, current_model))

            if result['tons'] != current_tonnage:
                error_list.append('Uploaded mech is %d tons, %s should be %d tons.' 
                                 % (result['tons'], current_chassis, current_tonnage))
            
            if len(error_list) > 0:
                result = {
                  'success' : False
                , 'errors'  : { 'SSW Data' : error_list }
                }
                form.instance.delete()
                return HttpResponse(json.dumps(result), status=400) 
            else:      
                return HttpResponse(json.dumps(result))  
        except BaseException as ex: 
            result = {
             'success' : False
            , 'errors'  : { 'SSW Data' : ['Failed to Parse Supplied File'] }
            }
            if settings.DEBUG:
                result['exception'] = ex.message
            
            form.instance.delete()
            return HttpResponse(json.dumps(result), status=400) 

    def dispatch(self, request, smw_id=0, *args, **kwargs):
        self.stablemechweek = get_object_or_404(models.StableMechWeek, id=smw_id)
        return super(OmniUploadMechView, self).dispatch(request, *args, **kwargs)


class MechRemoveAjaxView(MechModifyMixin, View):
    def post(self, request, smw_id=0):
        try:
            action = request.POST['action']
            if action == 'remove':
                self.stablemechweek.set_removed(True)
            elif action == 'core':
                self.stablemechweek.core_mech(True)
            else:
                return HttpResponse('Unrecognised action %s' % action, 400)

            result = { 'success' : True } 
            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 401)

class MechRefitFormView(MechModifyMixin, FormView):
    template_name = 'stablemanager/forms/refit_mech_form.html'
    form_class = forms.MechRefitForm

    def form_invalid(self, form):
        result = {
          'success' : False
        , 'non_field_errors'  : [error for error in form.non_field_errors()]
        , 'field_errors'  : dict([(field, error) for (field, error) in form.errors.items()])
        }

        for (field, errors) in form.errors.items(): 
            print '%s: %s' % (field, errors) 

        return HttpResponse(json.dumps(result))       

    def form_valid(self, form):
        if form.cleaned_data['mech_source'] == 'U':
            self.stableweek.add_custom_design(form.design) 

        self.stablemechweek.refit_to( form.design
                                    , add_ledger = form.cleaned_data['add_ledger']
                                    , failed_by  = form.cleaned_data['failed_by']
                                    )

        result = { 'success' : True }
        return HttpResponse(json.dumps(result))       

    def get_context_data(self, **kwargs):
        context = super(MechRefitFormView, self).get_context_data(**kwargs)
        
        context['stablemechweek'] = self.stablemechweek
        return context
    
class MechLoadoutsFormView(MechRefitFormView):
    template_name = 'stablemanager/forms/loadout_mech_form.html'
    
    def form_valid(self, form):
        if form.cleaned_data['mech_source'] == 'U':
            pass
            #TODO: Add Uploaded custom designs if needed
            
        models.StableMech.objects.create_mech( stable = self.stable
                                             , purchased_as = form.design
                                             , purchased_on = self.stableweek
                                             , create_ledger = form.cleaned_data['add_ledger']
                                             , delivery = form.cleaned_data['delivery'] 
                                             )
        result = { 'success' : True }
        return HttpResponse(json.dumps(result))   
    
class MechEditFormView(MechModifyMixin, TemplateView):
    template_name = 'stablemanager/forms/edit_mech_form.html'

    def get(self, request, *args, **kwargs):
        self.mechform = forms.MechChangeForm(instance=self.stablemechweek)
        return super(MechEditFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.mechform = forms.MechChangeForm(request.POST, instance=self.stablemechweek)

        if self.mechform.is_valid():
            self.mechform.save()

            mech = self.mechform.instance

            if self.mechform.cleaned_data['remove'] == 'remove':
               mech.set_removed(True);
            elif self.mechform.cleaned_data['remove'] == 'core':
               mech.core_mech(True);
            elif self.mechform.cleaned_data['remove'] == 'undo':
               mech.core_mech(False);
               

            return HttpResponse('Mech Changed', status=201)
        else:
            return super(MechEditFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MechEditFormView, self).get_context_data(**kwargs)
        
        context['mech'] = self.stablemechweek 
        context['mechform'] = self.mechform
        context['edit_url'] = self.stablemechweek.edit_url()
        
        return context

class MechRemoveConfigView(MechModifyMixin, View):
    def post(self, request, *args, **kwargs):
        removed = (request.POST['remove'].upper() == 'TRUE')

        if self.stablemechweek.config_for == None:
            result = {
              'success' : False
            , 'removed' : self.stablemechweek.removed
            , 'error'   : 'Selected Mech is not a Loadout'
            }
            return HttpResponse(json.dumps(result), 401)
        else:
            result = self.stablemechweek.set_removed(removed)

            result = {
              'success' : True
            , 'removed' : result
            }
            return HttpResponse(json.dumps(result))

