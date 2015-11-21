from django.forms.models import formset_factory
from django.forms import Form, CharField, IntegerField, HiddenInput, Select, ValidationError

from . import models
from solaris.warbook.mech.models import MechDesign
from solaris.campaign.models import BroadcastWeek

class SimpleMechPurchaseForm(Form):
    mech_name = CharField()
    mech_code = CharField(widget=Select)
    week_no = IntegerField(widget=HiddenInput(), initial=BroadcastWeek.objects.current_week().week_number)
        
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

InitialMechsForm = formset_factory(SimpleMechPurchaseForm)
