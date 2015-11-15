from django.forms.models import formset_factory
from django.forms import Form, CharField, Select

from . import models

class SimpleMechPurchaseForm(Form):
    mech_name = CharField()
    mech_code = CharField(widget=Select)
        
    def to_mech(self):
        pass
    
InitialMechsForm = formset_factory(SimpleMechPurchaseForm)