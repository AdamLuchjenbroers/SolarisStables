from django.forms.models import formset_factory
from django import forms 
from django.conf import settings

import uuid

from . import models
from solaris.warbook.mech.models import MechDesign
from solaris.campaign.models import BroadcastWeek
from solaris.utilities.loader import SSWLoader

class SimpleMechPurchaseForm(forms.Form):
    mech_name = forms.CharField()
    mech_code = forms.CharField(widget=forms.Select)
    week_no = forms.IntegerField(widget=forms.HiddenInput(), initial=BroadcastWeek.objects.current_week().week_number)
        
    def to_mech(self):
        pass

    def clean_week_no(self):
        week_no = self.cleaned_data['week_no']
        try:
            self.week = BroadcastWeek.objects.get(week_number=week_no)
        except BroadcastWeek.DoesNotExist:
            self.week = BroadcastWeek.objects.current_week()
            self.cleaned_data['week_no'] = self.week.week_number
        

    def clean(self):
        cleaned = super(SimpleMechPurchaseForm, self).clean()
        (mn, mc) = (cleaned['mech_name'], cleaned['mech_code'])

        try:
            self.design = MechDesign.objects.get(mech_name=mn, mech_code=mc)
        except MechDesign.DoesNotExist:
            raise forms.ValidationError('Unable to match design %s %s' % (mn, mc))
    
        return cleaned

class MechUploadOrPurchaseForm(forms.Form):
    mech_name = forms.CharField(required=False)
    mech_code = forms.CharField(widget=forms.Select, required=False)

    mech_ssw = forms.FileField(required=False)
    ssw_tempdata = forms.CharField(required=False)   
 
    mech_source = forms.CharField()
    as_purchase = forms.BooleanField(required=False, initial=True)

    def clean_mech_ssw(self):
        if 'mech_ssw' not in self.cleaned_data:
            return None

        ssw_upload_file = '%s' % uuid.uuid4()
        ssw_upload_tmp = '%s%s' % (settings.SSW_UPLOAD_TEMP, ssw_upload_file)
        with open(ssw_upload_tmp, 'wb+') as tmp_output:
            for chunk in self.cleaned_data['mech_ssw']:
                tmp_output.write(chunk)

        mech = SSWLoader(ssw_upload_file, basepath=settings.SSW_UPLOAD_TEMP)
        (mech_name, mech_code) = mech.get_model_details()
 
        if MechDesign.objects.filter(mech_name=mech_name, mech_code=mech_code).count() > 0:
            raise forms.ValidationError('Details for a %s %s are already present in the database' % (mech_name, mech_code))

        return mech

    def clean_mech_source(self):
        mech_source = self.cleaned_data['mech_source']
        if mech_source not in ('U', 'C'):
            raise forms.ValidationError('Unexpected value for mech source')
        return mech_source

    def clean_as_purchase(self):
        return (self.cleaned_data['as_purchase'] == True)

    def clean(self):
        cleaned_data = super(MechUploadOrPurchaseForm, self).clean()
        (mn, mc) = (cleaned_data['mech_name'], cleaned_data['mech_code'])

        if cleaned_data['mech_source'] not in ('C', 'U'):
            raise forms.ValidationError('Unable to load mech, source unspecified')         

        if cleaned_data['mech_source'] == 'U':
            if 'mech_ssw' in cleaned_data:
                cleaned_data['mech_ssw'].load_mechs(print_message=False, production_type='C') 
                (mn, mc) = self.cleaned_data['mech_ssw'].get_model_details()
            else:
                raise forms.ValidationError('Uploaded mech data not found')

        try:
            self.design = MechDesign.objects.get(mech_name=mn, mech_code=mc)
            return cleaned_data
        except MechDesign.DoesNotExist:
            raise forms.ValidationError('Unable to match design %s %s' % (mn, mc))

InitialMechsForm = forms.formset_factory(SimpleMechPurchaseForm)
