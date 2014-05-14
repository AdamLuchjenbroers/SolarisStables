'''
   ModelForm for validating Mech Data input loaded from SSW files
   This form is not intended to be rendered to a page
'''

from django.forms import ModelForm
from django.forms.models import model_to_dict

from solaris.warbook.mech.models import MechDesign, MechDesignLocation

class MechValidationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0],dict):
            args[0]['mech_key'] = '%s|%s' % (args[0]['mech_name'].lower(), args[0]['mech_code'].lower())
        
        super(MechValidationForm,self).__init__(*args, **kwargs)
        
    class Meta:
        model = MechDesign
        
class LocationValidationForm(ModelForm):
    
    class Meta:
        model = MechDesignLocation