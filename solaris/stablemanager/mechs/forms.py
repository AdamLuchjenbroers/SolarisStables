from django.forms.models import formset_factory
from django import forms 

from . import models
from solaris.warbook.mech.models import MechDesign
from solaris.campaign.models import BroadcastWeek

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
            raise ValidationError('Unable to match design %s %s' % (mn, mc))
    
        return cleaned

class MechUploadOrPurchaseForm(forms.Form):
    mech_name = forms.CharField(required=False)
    mech_code = forms.CharField(widget=forms.Select, required=False)

    mech_ssw = forms.FileField(required=False)
    
    mech_source = forms.ChoiceField(choices=[('Uploaded','U'), ('Catalog','C')])
    week_no = forms.IntegerField(widget=forms.HiddenInput)
    as_purchase = forms.BooleanField(required=False, initial=True)

    def __init__(self, week):
        super(MechUploadOrPurchaseForm, self).__init__(initial={
           'week_no' : week
        })

InitialMechsForm = forms.formset_factory(SimpleMechPurchaseForm)
