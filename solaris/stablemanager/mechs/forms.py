from django.forms.models import formset_factory
from django import forms 
from django.conf import settings

import uuid
from urllib import unquote

from . import models
from solaris.stablemanager.pilots.models import Pilot
from solaris.warbook.mech.models import MechDesign
from solaris.campaign.models import BroadcastWeek
from solaris.utilities.loader import SSWLoader

from solaris.files.models import TempMechFile
 
class SimpleMechPurchaseForm(forms.Form):
    mech_name = forms.CharField()
    mech_code = forms.CharField(widget=forms.Select)
    week_no = forms.IntegerField(widget=forms.HiddenInput(), initial=BroadcastWeek.objects.current_week().week_number)

    omni_loadout = forms.CharField(widget=forms.HiddenInput(), initial='Base')
        
    def to_mech(self):
        pass

    def clean_mech_name(self):
        return unquote(self.cleaned_data['mech_name'])

    def clean_mech_code(self):
        return unquote(self.cleaned_data['mech_code'])

    def clean_week_no(self):
        week_no = self.cleaned_data['week_no']
        try:
            self.week = BroadcastWeek.objects.get(week_number=week_no)
        except BroadcastWeek.DoesNotExist:
            self.week = BroadcastWeek.objects.current_week()
            self.cleaned_data['week_no'] = self.week.week_number
        return self.week
    
    def clean_omni_loadout(self):
        if 'omni_loadout' in self.cleaned_data and self.cleaned_data['omni_loadout'] != None:
            return self.cleaned_data['omni_loadout']
        else:
            return 'Base'

    def clean(self):
        cleaned = super(SimpleMechPurchaseForm, self).clean()
        if 'omni_loadout' in cleaned:
            (mn, mc, lo) = (cleaned['mech_name'], cleaned['mech_code'], cleaned['omni_loadout'])
        else:
            (mn, mc, lo) = (cleaned['mech_name'], cleaned['mech_code'], 'Base')

        try:
            self.design = MechDesign.objects.get(mech_name=mn, mech_code=mc, omni_loadout=lo)
        except MechDesign.DoesNotExist:
            self.design = None
            raise forms.ValidationError('Unable to match design %s %s (%s)' % (mn, mc, lo))
    
        return cleaned

class MechUploadOrPurchaseForm(forms.Form):
    mech_name = forms.CharField()
    mech_code = forms.CharField(widget=forms.Select)    
    omni_loadout = forms.CharField(required=False)
    mech_source = forms.CharField()
    
    temp_id = forms.ModelChoiceField(TempMechFile.objects.all(), required=False, to_field_name='id')
 
    as_purchase = forms.BooleanField(required=False, initial=True, label="Add as Purchase:")
    allmechs = forms.BooleanField(required=False, initial=False, label="Include Non-Stable Designs:")

    delivery = forms.IntegerField(initial=1, required=False, label="Delivery In (Weeks):")

    def clean_delivery(self):
        if 'delivery' not in self.cleaned_data or self.cleaned_data['delivery'] == None:
            return 0

        try:
            return max(0, int(self.cleaned_data['delivery']))
        except ValueError:
            raise forms.ValidationError('Delivery Delay should be a number')

    def clean_temp_id(self):
        
        if 'temp_id' not in self.cleaned_data or self.cleaned_data['temp_id'] == None:
            return None
        
        temp_id = self.cleaned_data['temp_id']
        
        if temp_id.design != None and not temp_id.is_omni:
            raise forms.ValidationError('Cannot accept uploaded mech - design already exists in database')
        
        return temp_id

    def clean_mech_source(self):
        mech_source = self.cleaned_data['mech_source']
        if mech_source not in ('U', 'C'):
            raise forms.ValidationError('Unexpected value for mech source')
        return mech_source

    def clean_as_purchase(self):
        return (self.cleaned_data['as_purchase'] == True)

    def clean_omni_loadout(self):
        if 'omni_loadout' not in self.cleaned_data or self.cleaned_data['omni_loadout'] == None:
            return 'Base'
        else:
            return self.cleaned_data['omni_loadout']

    def clean(self):
        cleaned_data = super(MechUploadOrPurchaseForm, self).clean()

        if 'omni_loadout' in cleaned_data:
            (mn, mc, lo) = (cleaned_data['mech_name'], cleaned_data['mech_code'], cleaned_data['omni_loadout'])
        else:
            (mn, mc, lo) = (cleaned_data['mech_name'], cleaned_data['mech_code'], 'Base')
            
        if cleaned_data['mech_source'] == 'U':
            if cleaned_data['temp_id'] == None:
                raise forms.ValidationError('No Uploaded Mech Data Found')
            
            if cleaned_data['temp_id'].is_omni:
                loadout = cleaned_data['temp_id'].loadouts.get(omni_loadout = lo)
                
                if loadout.design != None:
                    raise forms.ValidationError('Cannot accept uploaded loadout - config already exists in database')
            
                self.design = cleaned_data['temp_id'].load_config(lo, production_type='C')
            else:
                self.design = cleaned_data['temp_id'].load_design(production_type='C')
        else:
            # Production Design
            try:
                self.design = MechDesign.objects.get(mech_name=mn, mech_code=mc, omni_loadout=lo)
                return cleaned_data
            except MechDesign.DoesNotExist:
                raise forms.ValidationError('Unable to match design %(name)s %(code)s (%(loadout)s)'
                                           , params={ 'name' : mn, 'code' : mc, 'loadout' : lo}    )

class MechRefitForm(MechUploadOrPurchaseForm):
    add_ledger = forms.BooleanField(required=False, initial=True)
    failed_by  = forms.IntegerField(required=False, initial=0)

    def __init__(self, instance=None, *args, **kwargs):
        self.instance = instance
        super(MechRefitForm, self).__init__(*args, **kwargs)
  
    def clean_failed_by(self):
        if 'failed_by' not in self.cleaned_data or self.cleaned_data['failed_by'] == None:
            return 0

        try:
            return max(0, int(self.cleaned_data['failed_by']))
        except ValueError:
            raise forms.ValidationError('Roll Failure Margin should be a number')

    def clean_mech_name(self):
        # Won't be present for uploaded mechs, so this isn't necessarily a problem
        if 'mech_name' not in self.cleaned_data or self.cleaned_data['mech_name'] == "":
            return None

        print self.cleaned_data['mech_name']

        if self.instance.current_design.mech_name != self.cleaned_data['mech_name']:
            raise forms.ValidationError('Mech Chassis must match chassis of existing mech')

        return self.cleaned_data['mech_name']

    def clean_add_ledger(self):
        return (self.cleaned_data['add_ledger'] == True)
    
class MechLoadoutForm(MechRefitForm):
    def clean_add_ledger(self):
        return (self.cleaned_data['add_ledger'].upper == 'TRUE')
        

class MechChangeForm(forms.ModelForm):
    remove = forms.ChoiceField(widget=forms.RadioSelect, initial='keep')

    class Meta:
        model = models.StableMechWeek
        fields = ('signature_of', 'delivery')

    def remove_choices(self):
        if self.instance.cored or self.instance.removed:
            return (('keep', 'Don\'t Change'), ('undo', 'Undo Removal'))
        else:
            return (('keep', 'Don\'t Remove'), ('remove', 'Remove from Stable'), ('core', 'Mark Cored'))

    def pilot_choices(self):
        pilots = tuple([(p.pilot.id, str(p.pilot)) for p in self.instance.stableweek.pilots.all()]) 
        return ((None,'-- Non Signature --'),) + pilots 

    def __init__(self, *args, **kwargs):
        super(MechChangeForm, self).__init__(*args, **kwargs)
        self.fields['signature_of'].label = 'Signature Of:'
        self.fields['signature_of'].choices = self.pilot_choices()
        self.fields['delivery'].label = 'Delivery In (Weeks):'
        self.fields['remove'].choices = self.remove_choices()

    def clean_delivery(self):
        if 'delivery' not in self.cleaned_data or self.cleaned_data['delivery'] == "":
            return 0

        try:
            delivery = int(self.cleaned_data['delivery'])
            if delivery >= 0:
                return delivery
            else:
                raise ValidationError('Delivery delay cannot be negative')
        except ValueError:
            raise ValidationError('Delivery delay must be a number')

    def clean_signature_of(self):
        if 'signature_of' not in self.cleaned_data or self.cleaned_data['signature_of'] == "":
            return None

        pilot = self.cleaned_data['signature_of']

        if pilot == None:
            return None
        elif pilot.stable == self.instance.stableweek.stable:
            return pilot
        else:
            return ValidationError("Pilot does not belong to same stable as mech")
 
InitialMechsForm = forms.formset_factory(SimpleMechPurchaseForm)
