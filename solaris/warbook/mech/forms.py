'''
   ModelForm for validating Mech Data input loaded from SSW files
   This form is not intended to be rendered to a page
'''

from django.forms import ModelForm, CharField, IntegerField

from solaris.warbook.mech.models import MechDesign
from solaris.forms import SolarisForm

class MechValidationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0],dict):
            args[0]['mech_key'] = '%s|%s' % (args[0]['mech_name'].lower(), args[0]['mech_code'].lower())
        
        super(MechValidationForm,self).__init__(*args, **kwargs)
        
    class Meta:
        model = MechDesign
        
     
class MechSearchForm(SolarisForm):
    mech_name = CharField(label='Mech Name', required=False)
    mech_code = CharField(label='Mech Code', required=False)
    tonnage_low = IntegerField(label='Min Tons', required=False)
    tonnage_high = IntegerField(label='Max Tons', required=False)
    cost_low = IntegerField(label='Min Cost', required=False)
    cost_high = IntegerField(label='Max Cost', required=False)
    bv_low = IntegerField(label='Min BV', required=False)
    bv_high = IntegerField(label='Max BV', required=False)
